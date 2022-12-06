import aioredis
import async_timeout
import asyncio
import multiprocessing
from pathlib import Path
from typing import Optional
import uuid
import queue

import aioprocessing
from fastapi import FastAPI, Request, Form, status, WebSocket
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
import uvicorn

from redis_functions import publish_job_status, subscribe_to_job_status, update_job_data, get_job_data
from stable_diffusion_service import run_sd_service


q: Optional[aioprocessing.Queue] = None
job_publisher = aioredis.Redis.from_url("redis://localhost", decode_responses=True)


async def unicorn_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({'error': 'Too many requests.'}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


limiter = Limiter(key_func=get_remote_address)
QUEUE_MAX_SIZE = 30
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, unicorn_exception_handler)


@app.get("/jobs-in-queue/")
async def get_queue_length(request: Request):
    return JSONResponse({"jobs_in_queue": q.qsize(), 'max_queue_size': QUEUE_MAX_SIZE}, status_code=status.HTTP_200_OK)


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
        return JSONResponse({'job_id': job_id}, status_code=status.HTTP_202_ACCEPTED)


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
            except asyncio.TimeoutError:
                pass

    job_data = await get_job_data(job_id)
    if job_data:
        if job_data['status'] != 'finished':
            await subscribe_to_job_status(job_id, job_status_reader)
        else:
            await websocket.close(reason='Job finished.')
    else:
        await websocket.close(reason='Not found.')


if __name__ == "__main__":
    # Creating a process and exchanging queue with it for communication
    q = aioprocessing.AioQueue(QUEUE_MAX_SIZE)
    p = multiprocessing.Process(target=run_sd_service, args=(q,))
    p.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    p.terminate()
