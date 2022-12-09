import asyncio
import multiprocessing
import os
from pathlib import Path
from typing import Optional
import uuid
import queue

import aioprocessing
import aioredis
import async_timeout
from fastapi import FastAPI, Request, Form, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
import uvicorn
from websockets import ConnectionClosed

from redis_functions import publish_job_status, subscribe_to_job_status, update_job_data, get_job_data
from stable_diffusion_service import run_sd_service


q: Optional[aioprocessing.Queue] = None
job_publisher = aioredis.Redis.from_url("redis://localhost", decode_responses=True)


async def unicorn_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({'error': 'Too many requests.'}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


limiter = Limiter(key_func=get_remote_address)
QUEUE_MAX_SIZE = 30
QUEUE_STATE_WS_REFRESH_SECONDS = 30
api_params = {}
if os.getenv('ROOT_PATH', ''):
    api_params = {
        'root_path': os.getenv('ROOT_PATH'),
        'servers': [{"url": os.getenv('ROOT_PATH')}],
    }
app = FastAPI(**api_params)
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, unicorn_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    with open('static/index.html', 'r') as f:
        index_html = f.read()
    return HTMLResponse(content=index_html, status_code=status.HTTP_200_OK)


@app.get("/jobs-in-queue/")
async def get_queue_length(request: Request):
    return JSONResponse({"jobs_in_queue": q.qsize(), 'max_queue_size': QUEUE_MAX_SIZE}, status_code=status.HTTP_200_OK)


@app.websocket("/jobs-in-queue/ws/")
async def get_queue_length_ws(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json({"jobs_in_queue": q.qsize(), 'max_queue_size': QUEUE_MAX_SIZE})
            await asyncio.sleep(QUEUE_STATE_WS_REFRESH_SECONDS)
    except ConnectionClosed:
        pass
    except asyncio.CancelledError:
        await websocket.close()


@app.post("/txt2img/")
@limiter.limit("3/minute")
async def add_job_to_queue(request: Request, prompt: str = Form(...)):
    if not prompt:
        return JSONResponse({'error': 'Phrase cannot be empty.'}, status_code=status.HTTP_400_BAD_REQUEST)

    job_id = str(uuid.uuid4())
    try:
        q.put({'prompt': prompt, 'job_id': job_id}, block=False)
    except queue.Full:
        return JSONResponse({'error': 'Service busy. Try again later.'},
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    else:
        # Saving job's information
        await update_job_data(job_id, {'job_id': job_id, 'status': 'queued'})
        # Publishing job's status
        await publish_job_status(job_id, "queued")
        return_data = {
            'job_id': job_id,
            'job_detail_url': f'{request.scope.get("root_path")}{app.url_path_for("job_detail", job_id=job_id)}',
            'job_progress_feed': f'{request.scope.get("root_path")}{app.url_path_for("job_detail_ws", job_id=job_id)}',
        }
        return JSONResponse(return_data, status_code=status.HTTP_202_ACCEPTED)


@app.get("/txt2img/{job_id}/")
async def job_detail(request: Request, job_id: str):
    job_data = await get_job_data(job_id)
    if job_data:
        return JSONResponse(job_data, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse({'error': 'Not found'}, status_code=status.HTTP_404_NOT_FOUND)


@app.websocket("/txt2img/ws/{job_id}/")
async def job_detail_ws(job_id: str, websocket: WebSocket):
    await websocket.accept()
    img_path = f'images/{job_id}.png'

    async def job_status_reader(channel: aioredis.client.PubSub):
        while True:
            try:
                async with async_timeout.timeout(70):
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=60)
                    if message is not None:
                        img_exists = Path(img_path).exists()
                        job_message = {
                            "status": message['data'],
                            "progress": 100 if message['data'] == 'finished' else 0,
                            "img_url": img_path if img_exists else None,
                        }
                        await websocket.send_json(job_message)
                        if job_message['status'] == 'finished':
                            break
                    await asyncio.sleep(0.01)
            except ConnectionClosed:
                break
            except asyncio.TimeoutError:
                pass

    job_data = await get_job_data(job_id)
    if job_data:
        if job_data['status'] != 'finished':
            await subscribe_to_job_status(job_id, job_status_reader)
        await websocket.close(reason='Job finished.')
    else:
        await websocket.close(reason='Not found.')


if __name__ == "__main__":
    # Creating a process and exchanging queue with it for communication
    q = aioprocessing.AioQueue(QUEUE_MAX_SIZE)
    p = multiprocessing.Process(target=run_sd_service, args=(q,))
    p.start()
    root_path = os.getenv('ROOT_PATH', '')
    uvicorn.run(app, host="0.0.0.0", port=8000, root_path=root_path)
    p.terminate()
