from datetime import datetime, timedelta
from pathlib import Path
import random

import sqlalchemy.exc
from fastapi import APIRouter, Request, status, Form
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from rq import Queue
from rq.job import Job
from redis import Redis
from sqlmodel import Session, select

from rent_gpu.requestor.db import engine, Offer, OfferStatus, MACHINE_LIFETIME
from rent_gpu.requestor.ssh_proxy import rent_server as rent_server_pytorch_ssh
from rent_gpu.requestor.automatic_proxy import rent_server as rent_server_automatic

redis_conn = Redis()
q = Queue(connection=redis_conn)
router = APIRouter()
api_dir = Path(__file__).parent.joinpath('..').absolute()
templates = Jinja2Templates(directory="rent_gpu/requestor/api/templates")


@router.get("/", response_class=HTMLResponse)
async def list_offers(request: Request):
    with Session(engine) as session:
        offers = session.exec(select(Offer))
        return templates.TemplateResponse("home.html", {"request": request, "offers": offers})


@router.post("/machines/{provider_id}/rent/")
async def rent(provider_id: str, package: str = Form(...)):
    # Random port is good enough for PoC
    port = random.randint(2000, 2999)
    vm_run_function = rent_server_automatic if package == 'automatic' else rent_server_pytorch_ssh
    job = Job.create(vm_run_function, (provider_id, port), connection=redis_conn, timeout='100d')
    with Session(engine) as session:
        try:
            offer = session.exec(
                select(Offer)
                .where(Offer.provider_id == provider_id, Offer.status == OfferStatus.FREE)
            ).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            offer.status = OfferStatus.RESERVED
            offer.job_id = job.get_id()
            offer.package = package
            offer.port = port
            offer.started_at = datetime.now()
            session.add(offer)
            session.commit()
            q.enqueue_job(job)
    return RedirectResponse(router.url_path_for("provider_status", provider_id=provider_id),
                            status_code=status.HTTP_302_FOUND)


@router.post("/machines/{provider_id}/terminate/")
async def terminate(provider_id: str):
    with Session(engine) as session:
        try:
            offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            if offer.status == OfferStatus.READY:
                offer.status = OfferStatus.TERMINATING
                session.add(offer)
                session.commit()
            else:
                return JSONResponse({'error': f'Cannot stop machine in status {offer.status}.'},
                                    status_code=status.HTTP_400_BAD_REQUEST)
    return RedirectResponse(router.url_path_for("provider_status", provider_id=provider_id),
                            status_code=status.HTTP_302_FOUND)


@router.get("/machines/{provider_id}/", response_class=HTMLResponse)
async def provider_status(provider_id: str, request: Request):
    with Session(engine) as session:
        try:
            offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            expire_in = max(offer.started_at + MACHINE_LIFETIME - datetime.now(), timedelta(seconds=0))
            return templates.TemplateResponse("offer-details.html", {"request": request, "offer": offer,
                                                                     "expire_in": expire_in})
