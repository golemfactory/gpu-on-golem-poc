from datetime import timedelta
import logging

from django.core.cache import cache
from django.utils import timezone
from redis.exceptions import LockError

from clusters.models import Cluster, Worker, Provider
from clusters.providers.runpod_provider import (create_runpod_worker, terminate_runpod_worker, is_worker_reachable,
                                                worker_exists, WORKER_CREATION_TIMEOUT)
from rent_golem.celery import app

WORKER_LOCK_NAME = "WORKER_LOCK_{worker_id}"
AFTER_CLUSTER_TERMINATED_GRACE_PERIOD = timedelta(minutes=5)

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


def check_worker_health(worker: Worker) -> bool:
    status_modified = False

    if worker.provider == Provider.RUNPOD:
        exists = worker_exists(worker)
        is_reachable = is_worker_reachable(worker)

        if exists and is_reachable:
            current_status = Worker.Status.OK
        else:
            current_status = Worker.Status.BAD

        if worker.status != current_status:
            status_modified = True
            worker.status = current_status
            worker.save(update_fields=['status'])
    else:
        logger.error(f'Cannot check worker health. Unrecognized provider: {worker.provider}.')

    return status_modified


@app.task()
def stop_orphaned_workers():
    orphaned_workers = Worker.objects.filter(
        cluster__status=Cluster.Status.TERMINATED,
        last_update__lt=(timezone.now() - AFTER_CLUSTER_TERMINATED_GRACE_PERIOD),
        status__in={Worker.Status.STARTING, Worker.Status.OK, Worker.Status.BAD}
    )
    for worker in orphaned_workers:
        logger.warning(f'Detected orphaned worker: {worker}. Terminating.')
        terminate_worker.delay(worker.id)


# TODO: write migration which adds above task to schedule:
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
#
# schedule, created = IntervalSchedule.objects.create(
#     every=5,
#     period=IntervalSchedule.MINUTES,
# )
# PeriodicTask.objects.create(
#     interval=schedule,
#     name='Importing contacts',
#     task='clusters.worker_tasks.stop_orphaned_workers',
# )
