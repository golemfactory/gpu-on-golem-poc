import os
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import sentry_sdk
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.routers import jobs, monitoring
from config import SENTRY_DSN


sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0)


async def throttling_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({'error': 'Too many requests.'}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


data_dir = Path(os.environ.get("GPUOG_DATA_DIR") or Path(__file__).parent)
frontend_dir = Path(os.environ.get("GPUOG_FRONTEND_DIR") or Path(__file__).parent)


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.include_router(jobs.router)
app.include_router(monitoring.router)
app.mount("/images", StaticFiles(directory=data_dir.joinpath('images').resolve()), name="images")
app.mount("/static", StaticFiles(directory=frontend_dir.joinpath('static').resolve()), name="static")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, throttling_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    with open(frontend_dir.joinpath('static/index.html'), 'r') as f:
        index_html = f.read()
    return HTMLResponse(content=index_html, status_code=status.HTTP_200_OK)
