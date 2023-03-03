from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from rent_gpu.requestor.api.routers import offers


app = FastAPI()
# app.include_router(offers.router)
# app.mount("/images", StaticFiles(directory=Path(__file__).parent.joinpath('images').resolve()), name="images")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.joinpath('static').resolve()), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="rent_gpu/requestor/api/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    offers = [
        {'provider_id': '0x7003e7d793b5c054e5a4c6041bd7592cf941741f', 'name': 'golem-3060-1', 'card': 'GA106 [GeForce RTX 3060 Lite Hash Rate]'},
        {'provider_id': '0x6003e7d793b5c054e5a4c6041bd7592cf941741f', 'name': 'golem-3090-2', 'card': 'GA106 [GeForce RTX 3090 Lite Hash Rate]'},
        {'provider_id': '0x8003e7d793b5c054e5a4c6041bd7592cf941741f', 'name': 'golem-3070-3', 'card': 'GA106 [GeForce RTX 3070 Lite Hash Rate]'},
    ]
    return templates.TemplateResponse("base.html", {"request": request, "offers": offers})
