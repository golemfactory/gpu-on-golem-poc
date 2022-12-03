import multiprocessing
from pathlib import Path
from typing import Optional
import uuid

from fastapi import FastAPI, Request, Form, status, Response
from fastapi.staticfiles import StaticFiles
from redis import Redis
from rq import Queue
from rq.job import Job
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.templating import Jinja2Templates
import uvicorn

from stable_diffusion_service import run_sd_service


q: Optional[multiprocessing.Queue] = None
redis_conn = Redis()
job_queue = Queue(connection=redis_conn)


async def unicorn_exception_handler(request: Request, exc: RateLimitExceeded):
    return templates.TemplateResponse(
        "throttling.html",
        {
            "request": request,
            "expire": 1,
        }
    )


limiter = Limiter(key_func=get_remote_address)
QUEUE_MAX_SIZE = 30
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, unicorn_exception_handler)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, 'root_path': request.scope.get("root_path")})


@app.post("/txt2img/")
@limiter.limit("3/minute")
async def add_job_to_queue(request: Request, prompt: str = Form(...)):
    if len(job_queue) >= QUEUE_MAX_SIZE:
        return Response({'error': 'Service busy. Try again later.'}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    else:
        uuid_str = str(uuid.uuid4())
        if prompt:
            q.put(prompt)
            return Response({'job_id': uuid_str}, status_code=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Phrase cannot be empty.'}, status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/txt2img/{job_id}/")
async def job_detail(request: Request, job_id: str, prompt: str = ""):
    # TODO: must be fetched from somewhere else - probably DB.
    job = Job.fetch(job_id, connection=redis_conn)
    img_path = f'images/{job_id}.png'
    img_exists = Path(img_path).exists()
    job_status_to_status = {
        'queued': 'Processing',
        'started': 'Processing',
        'deferred': 'Processing',
        'finished': 'Ready' if img_exists else 'Failed',
        'stopped': 'Failed',
        'scheduled': 'Processing',
        'canceled': 'Failed',
        'failed': 'Failed',
    }
    task_status = job_status_to_status[job.get_status()]
    return templates.TemplateResponse(
        "job-detail.html",
        {
            "request": request,
            'root_path': request.scope.get("root_path"),
            "prompt": prompt,
            "status": task_status,
            "img_path": img_path,
        })


if __name__ == "__main__":
    # Creating a process and exchanging queue with it for communication
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_sd_service, args=(q,))
    p.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
