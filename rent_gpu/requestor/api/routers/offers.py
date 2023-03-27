from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import Optional
import uuid

import sqlalchemy.exc
from fastapi import APIRouter, Request, status, Form, Cookie
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from rq import Queue
from rq.job import Job
from redis import Redis
from sqlmodel import Session, select

from rent_gpu.requestor.db import engine, Offer, OfferStatus, MACHINE_LIFETIME
from rent_gpu.requestor.ssh_proxy import rent_server as rent_server_pytorch_ssh
from rent_gpu.requestor.automatic_proxy import rent_server as rent_server_automatic
from rent_gpu.requestor.jupyter_proxy import rent_server as rent_server_jupyter

redis_conn = Redis()
q = Queue(connection=redis_conn)
router = APIRouter()
api_dir = Path(__file__).parent.joinpath('..').absolute()
templates = Jinja2Templates(directory="rent_gpu/requestor/api/templates")


@router.get("/", response_class=HTMLResponse)
async def list_offers(request: Request, access_key: Optional[str] = Cookie(None)):
    with Session(engine) as session:
        offers = session.exec(select(Offer))
        accessible_offers = filter(lambda o: o.has_access(access_key), offers)
        response = templates.TemplateResponse("home.html", {"request": request, "offers": accessible_offers})
        if not access_key:
            expires = datetime.utcnow() + timedelta(days=30)
            response.set_cookie('access_key', value=str(uuid.uuid4()), httponly=True,
                                expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        return response


@router.post("/machines/{provider_id}/rent/")
async def rent(provider_id: str, package: str = Form(...), access_key: Optional[str] = Cookie(None)):
    package_to_function_map = {
        'pytorch': rent_server_pytorch_ssh,
        'automatic': rent_server_automatic,
        'jupyter': rent_server_jupyter,
    }
    # Random port is good enough for PoC
    port = random.randint(2000, 2999)
    vm_run_function = package_to_function_map[package]
    job = Job.create(vm_run_function, (provider_id, port), connection=redis_conn, timeout='100d')
    with Session(engine) as session:
        try:
            offer = session.exec(
                select(Offer)
                .where(Offer.provider_id == provider_id, Offer.status == OfferStatus.FREE)
            ).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found. Might be also already reserved.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            offer.status = OfferStatus.RESERVED
            offer.job_id = job.get_id()
            offer.package = package
            offer.port = port
            offer.started_at = datetime.now()
            offer.reserved_by = access_key
            session.add(offer)
            session.commit()
            q.enqueue_job(job)
    return RedirectResponse(router.url_path_for("provider_status", provider_id=provider_id),
                            status_code=status.HTTP_302_FOUND)


@router.post("/machines/{provider_id}/terminate/")
async def terminate(provider_id: str, access_key: Optional[str] = Cookie(None)):
    with Session(engine) as session:
        try:
            offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            if not offer.has_access(access_key):
                return JSONResponse({'error': f'Provider id: {provider_id} reserved by someone else.'},
                                    status_code=status.HTTP_403_FORBIDDEN)
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
async def provider_status(provider_id: str, request: Request, access_key: Optional[str] = Cookie(None)):
    with Session(engine) as session:
        try:
            offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
        except sqlalchemy.exc.NoResultFound:
            return JSONResponse({'error': f'Provider id: {provider_id} not found.'},
                                status_code=status.HTTP_404_NOT_FOUND)
        else:
            if not offer.has_access(access_key):
                return JSONResponse({'error': f'Provider id: {provider_id} reserved by someone else.'},
                                    status_code=status.HTTP_403_FORBIDDEN)
            else:
                if offer.started_at:
                    expire_in = max(offer.started_at + MACHINE_LIFETIME - datetime.now(), timedelta(seconds=0))
                else:
                    expire_in = None
                return templates.TemplateResponse("offer-details.html", {"request": request, "offer": offer,
                                                                         "expire_in": expire_in})
