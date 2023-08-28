import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Worker, Provider
from clusters.providers.runpod_provider import (create_runpod_worker, terminate_runpod_worker, is_worker_reachable,
                                                worker_exists, WORKER_CREATION_TIMEOUT)
from rent_golem.celery import app

WORKER_LOCK_NAME = "WORKER_LOCK_{worker_id}"

logger = logging.getLogger(__name__)

@app.task()
def create_worker(worker_id: int):
    lock_name = WORKER_LOCK_NAME.format(worker_id=worker_id)
    try:
        with cache.lock(lock_name, blocking_timeout=0, timeout=WORKER_CREATION_TIMEOUT.total_seconds()):
            worker = Worker.objects.get(id=worker_id)
            if worker.provider == Provider.RUNPOD:
                create_runpod_worker(worker)
            else:
                logger.error(f'Cannot create worker. Unrecognized provider: {worker.provider}.')
    except LockError:
        logger.error(f"'{lock_name}' already locked.")


@app.task(
    autoretry_for=(LockError,),
    retry_kwargs={'max_retries': 3, 'countdown': 2}
)
def terminate_worker(worker_id: int):
    lock_name = WORKER_LOCK_NAME.format(worker_id=worker_id)
    with cache.lock(lock_name, blocking_timeout=0, timeout=WORKER_CREATION_TIMEOUT.total_seconds()):
        worker = Worker.objects.get(id=worker_id)
        if worker.provider == Provider.RUNPOD:
            terminate_runpod_worker(worker)
        else:
            logger.error(f'Cannot terminate worker. Unrecognized provider: {worker.provider}.')


def check_worker_health(worker: Worker):
    if worker.provider == Provider.RUNPOD:
        exists = worker_exists(worker)
        is_reachable = is_worker_reachable(worker)

        if exists and is_reachable:
            status = Worker.Status.OK
        else:
            status = Worker.Status.BAD

        worker.status = status
        worker.save(update_fields=['status'])
    else:
        logger.error(f'Cannot check worker health. Unrecognized provider: {worker.provider}.')
