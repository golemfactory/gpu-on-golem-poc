from fastapi import FastAPI, Request, Form, status
from typing import Union
from stable_diffusion import generate_image

import uuid, rq

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/text2img/")
async def add_item_to_queue(request: Request, prompt: str = Form(...)): #TODO How FastAPI knows which string from Form to take? What if there is more "prompt" named text inputs? Are names unique in HTML (same as IDs)?  
    uuid_str = str(uuid.uuid4())
    url = app.url_path_for("read_item", uuid=uuid_str)
    url += ("?prompt=" + prompt)
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)

@app.get("/text2img/{uuid}/")
async def read_item(request: Request, uuid: str, prompt: str = ""):
    return templates.TemplateResponse(
        "job-detail.html", 
        {
            "request": request, 
            "prompt": prompt, 
            "status": task_status, 
            "img_path": img_path
        })