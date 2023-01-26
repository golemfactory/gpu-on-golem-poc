import asyncio

from fastapi import APIRouter, Request, status, WebSocket
from fastapi.responses import JSONResponse
from websockets import ConnectionClosed

from api.redis_functions import get_service_data, jobs_queue

QUEUE_STATE_WS_REFRESH_SECONDS = 5

router = APIRouter()


@router.get("/monitoring/cluster/")
async def monitoring(request: Request):
    service_data = await get_service_data()
    return JSONResponse(service_data, status_code=status.HTTP_200_OK)


@router.get("/jobs-in-queue/")
async def get_queue_length(request: Request):
    queue_size = await jobs_queue.qsize()
    return JSONResponse({"jobs_in_queue": queue_size, 'max_queue_size': jobs_queue.max_size},
                        status_code=status.HTTP_200_OK)


@router.websocket("/jobs-in-queue/ws/")
async def get_queue_length_ws(websocket: WebSocket):
    await websocket.accept()

    hold_off_user = False
    try:
        while True:
            queue_size = await jobs_queue.qsize()

            if hold_off_user and queue_size < 0.7 * jobs_queue.max_size:
                hold_off_user = False

            if queue_size >= jobs_queue.max_size:
                hold_off_user = True

            msg = {
                "jobs_in_queue": queue_size,
                'max_queue_size': jobs_queue.max_size,
                'hold_off_user': hold_off_user,
            }
            await websocket.send_json(msg)
            await asyncio.sleep(QUEUE_STATE_WS_REFRESH_SECONDS)
    except ConnectionClosed:
        pass
    except asyncio.CancelledError:
        await websocket.close()
