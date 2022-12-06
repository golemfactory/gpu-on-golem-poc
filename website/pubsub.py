import aioredis
from typing import Callable, Awaitable


job_publisher = aioredis.Redis.from_url("redis://localhost", decode_responses=True)
redis = aioredis.Redis.from_url("redis://localhost", max_connections=10, decode_responses=True)


async def publish_job_status(job_id: str, status: str) -> None:
    await job_publisher.publish(get_job_channel(job_id), status)


# Not tested
async def subscribe_to_job_status(job_id: str, reader_func: Callable[[aioredis.client.PubSub], Awaitable[None]]) -> None:
    psub = redis.pubsub()
    async with psub as p:
        await p.subscribe(get_job_channel(job_id))
        await reader_func(p)
        await p.unsubscribe(get_job_channel(job_id))


def get_job_channel(job_id: str) -> str:
    return f'channel:{job_id}'
