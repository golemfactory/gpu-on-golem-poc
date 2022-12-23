import multiprocessing
import os
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
import uvicorn

from api.stable_diffusion.service import run_sd_service
from api.routers import jobs, monitoring


async def throttling_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({'error': 'Too many requests.'}, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


limiter = Limiter(key_func=get_remote_address)
api_params = {}
if os.getenv('ROOT_PATH', ''):
    api_params = {
        'root_path': os.getenv('ROOT_PATH'),
        'servers': [{"url": os.getenv('ROOT_PATH')}],
    }
app = FastAPI(**api_params)
app.include_router(jobs.router)
app.include_router(monitoring.router)
app.mount("/images", StaticFiles(directory=Path(__file__).parent.joinpath('images').resolve()), name="images")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.joinpath('static').resolve()), name="static")
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
    with open(Path(__file__).parent.joinpath('static/index.html'), 'r') as f:
        index_html = f.read()
    return HTMLResponse(content=index_html, status_code=status.HTTP_200_OK)

import logging.config
log_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s'
        },
    },
    'handlers': {
        'logconsole': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.StreamHandler',
        },
        'logfile': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': Path(__file__).parent.joinpath('app.log').resolve(),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['logconsole', 'logfile'],
        }
    }
}
# logging.config.dictConfig(log_config)


if __name__ == "__main__":
    p = multiprocessing.Process(target=run_sd_service)
    p.start()
    root_path = os.getenv('ROOT_PATH', '')
    working_dir = Path(__file__).parent.resolve()
    uvicorn.run(app, host="0.0.0.0", port=8000, root_path=root_path)
    p.terminate()
