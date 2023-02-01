import json
import queue
from typing import Callable, Awaitable

import aioredis
from yapapi.services import ServiceState

from api.choices import JobStatus


JOBS_QUEUE_MAX_SIZE = 30
SERVICE_INFO_RETENCY_SECONDS = 60 * 20
JOB_INFO_RETENCY_SECONDS = 60 * 60 * 24
PROVIDER_PROCESSING_TIME_MAX_RECORDS = 30
job_publisher = aioredis.Redis.from_url("redis://localhost", decode_responses=True)
redis = aioredis.Redis.from_url("redis://localhost", decode_responses=True)


async def get_job_data(job_id: str):
    raw_data = await redis.get(get_job_data_key(job_id))
    if raw_data:
        return json.loads(raw_data)
    else:
        return None


async def update_job_data(job_id: str, obj: dict) -> None:
    try:
        async with redis.lock(f"job_data_lock:{job_id}", timeout=2, blocking_timeout=10):
            data = await get_job_data(job_id)
            if data:
                data.update(obj)
            else:
                data = obj
            raw_data = json.dumps(data)
            await redis.set(get_job_data_key(job_id), raw_data, ex=JOB_INFO_RETENCY_SECONDS)
    except aioredis.exceptions.LockError as e:
        print(f'LockError: {e}')
    else:
        await _publish_job_status(job_id, data)


async def subscribe_to_job_status(job_id: str, reader_func: Callable[[aioredis.client.PubSub], Awaitable[None]]) -> None:
    psub = redis.pubsub()
    async with psub as p:
        await p.subscribe(get_job_channel(job_id))
        await reader_func(p)
        await p.unsubscribe(get_job_channel(job_id))


async def _publish_job_status(job_id: str, job_data: dict):
    message_str = json.dumps(job_data)
    await job_publisher.publish(get_job_channel(job_id), message_str)


def get_job_channel(job_id: str) -> str:
    return f'channel:{job_id}'


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


def get_provider_time_key(provider_id: str):
    return f'provider-times:{provider_id}'


async def set_provider_processing_time(provider_id: str, time: float) -> None:
    await redis.lpush(get_provider_time_key(provider_id), time)
    # Keeping list length limited
    await redis.ltrim(get_provider_time_key(provider_id), 0, PROVIDER_PROCESSING_TIME_MAX_RECORDS - 1)


async def get_providers_processing_times() -> dict:
    service_data = await get_service_data()
    instances = service_data['cluster']['instances'] if 'cluster' in service_data else []
    return {
        instance['provider_id']:
            [
                float(t) for t in await redis.lrange(get_provider_time_key(instance['provider_id']), 0, -1)
            ]
        for instance in instances
        if instance['state'] == ServiceState.running.name
    }


class AsyncRedisQueue:
    def __init__(self, name, namespace='queue', max_size=None):
        self._db = redis
        self.key = '%s:%s' % (namespace, name)
        self.max_size = max_size

    async def qsize(self):
        return await self._db.llen(self.key)

    async def put(self, item: dict):
        if await self.qsize() >= self.max_size:
            raise queue.Full
        else:
            item_serialized = json.dumps(item)
            return await self._db.rpush(self.key, item_serialized)

    async def get(self, timeout=0):
        item = await self._db.blpop(self.key, timeout=timeout)
        if item:
            item = json.loads(item[1])
        return item

    async def notify_queued(self):
        """Notify all queued jobs listeners that their job changed position in the queue."""

        elements = await self._db.lrange(self.key, 0, -1)
        if elements:
            for i, el in enumerate(elements):
                job = json.loads(el)
                job_update_data = {
                    'status': JobStatus.QUEUED.value,
                    'queue_position': i+1,
                    'jobs_in_queue': len(elements),
                }
                await update_job_data(job['job_id'], job_update_data)


jobs_queue = AsyncRedisQueue('jobs', max_size=JOBS_QUEUE_MAX_SIZE)
