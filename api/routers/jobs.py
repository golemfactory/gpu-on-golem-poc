import asyncio
import json
from pathlib import Path
import queue
import uuid

import aioredis
import async_timeout
from fastapi import APIRouter, Form, Request, status, WebSocket
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from websockets import ConnectionClosed

from api.choices import JobStatus
from api.redis_functions import publish_job_status, subscribe_to_job_status, update_job_data, get_job_data, jobs_queue


api_dir = Path(__file__).parent.joinpath('..').absolute()
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/txt2img/")
@limiter.limit("5/minute")
async def add_job_to_queue(request: Request, prompt: str = Form(...)):
    if not prompt:
        return JSONResponse({'error': 'Phrase cannot be empty.'}, status_code=status.HTTP_400_BAD_REQUEST)

    job_id = str(uuid.uuid4())
    with open(api_dir / 'requests.log', 'a') as f:
        f.write(f'{job_id} {prompt}\n')

    try:
        await jobs_queue.put({'prompt': prompt, 'job_id': job_id})
    except queue.Full:
        return JSONResponse({'error': 'Service busy. Try again later.'},
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    else:
        # Saving job's information
        await update_job_data(job_id, {'job_id': job_id, 'status': JobStatus.QUEUED.value})
        # Publishing job's status
        await publish_job_status(job_id, JobStatus.QUEUED.value)
        return_data = {
            'job_id': job_id,
            'status': JobStatus.QUEUED.value,
            'job_detail_url': request.url_for("job_detail", job_id=job_id),
            'job_progress_feed': request.url_for("job_detail_ws", job_id=job_id),
        }
        return JSONResponse(return_data, status_code=status.HTTP_202_ACCEPTED)


@router.get("/txt2img/{job_id}/")
async def job_detail(request: Request, job_id: str):
    job_data = await get_job_data(job_id)
    if job_data:
        return JSONResponse(job_data, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse({'error': 'Not found'}, status_code=status.HTTP_404_NOT_FOUND)


@router.websocket("/txt2img/ws/{job_id}/")
async def job_detail_ws(job_id: str, websocket: WebSocket):
    await websocket.accept()
    final_img_path = f'images/{job_id}.png'

    async def job_status_reader(channel: aioredis.client.PubSub):
        while True:
            try:
                async with async_timeout.timeout(70):
                    message = await channel.get_message(ignore_subscribe_messages=True, timeout=60)
                    if message is not None:
                        message_data = json.loads(message['data'])
                        local_img_path = api_dir / final_img_path
                        final_img_exists = local_img_path.exists()
                        job_message = {
                            "status": message_data['status'],
                            "queue_position": message_data['queue_position'],
                            "provider": message_data['provider'],
                            "progress": message_data['progress'],
                            "img_url": final_img_path if final_img_exists else None,
                            "intermediary_images": message_data['intermediary_images'],
                        }
                        await websocket.send_json(job_message)
                        if job_message['status'] == JobStatus.FINISHED.value:
                            break
                    await asyncio.sleep(0.01)
            except ConnectionClosed:
                break
            except asyncio.TimeoutError:
                pass

    job_data = await get_job_data(job_id)
    if job_data:
        if job_data['status'] != JobStatus.FINISHED.value:
            await subscribe_to_job_status(job_id, job_status_reader)
        await websocket.close(reason='Job finished.')
    else:
        await websocket.close(reason='Not found.')
