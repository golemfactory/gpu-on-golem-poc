import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Worker, Provider
from clusters.providers.runpod_provider import create_runpod_worker, terminate_runpod_worker
from rent_golem.celery import app

WORKER_LOCK_NAME = "WORKER_LOCK_{worker_id}"


logger = logging.getLogger(__name__)

@app.task()
def create_worker(worker_id: int):
    lock_name = WORKER_LOCK_NAME.format(worker_id=worker_id)
    try:
        with cache.lock(lock_name, blocking=False):
            worker = Worker.objects.get(worker_id)
            if worker.provider is Provider.RUNPOD:
                create_runpod_worker(worker)
            else:
                logger.error(f'Cannot create worker. Unrecognized provider: {worker.provider}.')
    except LockError:
        logger.error(f"'{lock_name}' already locked.")


@app.task()
def terminate_worker(worker_id: int):
    lock_name = WORKER_LOCK_NAME.format(worker_id=worker_id)
    try:
        with cache.lock(lock_name, blocking=False):
            worker = Worker.objects.get(worker_id)
            if worker.provider is Provider.RUNPOD:
                terminate_runpod_worker(worker)
            else:
                logger.error(f'Cannot terminate worker. Unrecognized provider: {worker.provider}.')
    except LockError:
        logger.error(f"'{lock_name}' already locked.")
