import json
from typing import Callable, Awaitable

import aioredis


SERVICE_INFO_RETENCY_SECONDS = 60 * 20
JOB_INFO_RETENCY_SECONDS = 60 * 60 * 24
job_publisher = aioredis.Redis.from_url("redis://localhost", decode_responses=True)
redis = aioredis.Redis.from_url("redis://localhost", max_connections=10, decode_responses=True)


async def publish_job_status(job_id: str, status: str, progress: int = 0, images: list = None) -> None:
    message = {
        'status': status,
        'progress': progress,
        'intermediary_images': [] if images is None else images
    }
    message_str = json.dumps(message)
    await job_publisher.publish(get_job_channel(job_id), message_str)


async def subscribe_to_job_status(job_id: str, reader_func: Callable[[aioredis.client.PubSub], Awaitable[None]]) -> None:
    psub = redis.pubsub()
    async with psub as p:
        await p.subscribe(get_job_channel(job_id))
        await reader_func(p)
        await p.unsubscribe(get_job_channel(job_id))


def get_job_channel(job_id: str) -> str:
    return f'channel:{job_id}'


async def get_job_data(job_id: str):
    raw_data = await redis.get(get_job_data_key(job_id))
    if raw_data:
        return json.loads(raw_data)
    else:
        return None


async def update_job_data(job_id: str, obj: dict) -> None:
    data = await get_job_data(job_id)
    if data:
        data.update(obj)
    else:
        data = obj
    raw_data = json.dumps(data)
    await redis.set(get_job_data_key(job_id), raw_data, ex=JOB_INFO_RETENCY_SECONDS)


def get_job_data_key(job_id: str) -> str:
    return f'job:{job_id}'


async def set_service_data(data: dict) -> None:
    raw_data = json.dumps(data)
    await redis.set('service-state', raw_data, ex=SERVICE_INFO_RETENCY_SECONDS)


async def get_service_data() -> dict:
    raw_data = await redis.get('service-state')
    if raw_data:
        return json.loads(raw_data)
    else:
        return {}
