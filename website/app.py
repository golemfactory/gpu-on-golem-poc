import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

from redis import Redis
from rq import Queue
from rq.job import Job

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from stable_diffusion import generate_image

async def unicorn_exception_handler(request: Request, exc: RateLimitExceeded):
    return templates.TemplateResponse(
        "throttling.html",
        {
            "request": request,
            "expire": 1,
        }
    )

redis_conn = Redis()
limiter = Limiter(key_func=get_remote_address)
q = Queue(connection=redis_conn)
templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, unicorn_exception_handler)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/txt2img/")
@limiter.limit("3/minute")
async def add_job_to_queue(request: Request, prompt: str = Form(...)):
    uuid_str = str(uuid.uuid4())
    q.enqueue(generate_image, prompt, uuid_str, job_id=uuid_str)
    url = app.url_path_for("job_detail", job_id=uuid_str)
    url += ("?prompt=" + prompt)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get("/txt2img/{job_id}/")
async def job_detail(request: Request, job_id: str, prompt: str = ""):
    job = Job.fetch(job_id, connection=redis_conn)
    img_path = f'/images/{job_id}.png'
    img_exists = Path(f'images/{job_id}.png').exists()
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
            "prompt": prompt,
            "status": task_status,
            "img_path": img_path,
        })
