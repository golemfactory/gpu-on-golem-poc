import json
from pathlib import Path
import queue
import uuid

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.choices import JobStatus
from redis_db.functions import (subscribe_to_job_status, update_job_data, get_job_data, jobs_queue,
                                get_providers_processing_times)


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
        queue_position = await jobs_queue.put({'prompt': prompt, 'job_id': job_id})
    except queue.Full:
        return JSONResponse({'error': 'Service busy. Try again later.'},
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        # Saving job's information
        await update_job_data(job_id, {'job_id': job_id, 'status': JobStatus.QUEUED.value,
                                       'queue_position': queue_position, 'jobs_in_queue': queue_position})
        return_data = {
            'job_id': job_id,
            'status': JobStatus.QUEUED.value,
            'queue_position': queue_position,
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
