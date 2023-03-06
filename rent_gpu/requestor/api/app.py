from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rent_gpu.requestor.api.routers import offers


app = FastAPI()
app.include_router(offers.router)
# app.mount("/images", StaticFiles(directory=Path(__file__).parent.joinpath('images').resolve()), name="images")
# app.mount("/static", StaticFiles(directory=Path(__file__).parent.joinpath('static').resolve()), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
