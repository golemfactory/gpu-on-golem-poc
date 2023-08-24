import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Cluster, Worker, Provider
from clusters.runner import ClusterRunner
from clusters.providers.runpod_provider import create_runpod_worker, terminate_runpod_worker
from rent_golem.celery import app


logger = logging.getLogger(__name__)

CLUSTER_LOCK_NAME = "CLUSTER_RUN_LOCK_{cluster_id}"
WORKER_LOCK_NAME = "WORKER_LOCK_{worker_id}"


@app.task(bind=True)
def run_cluster(self, cluster_id: int):
    lock_name = CLUSTER_LOCK_NAME.format(cluster_id=cluster_id)
    try:
        with cache.lock(lock_name, blocking=False):
            try:
                cluster = Cluster.objects.get(id=cluster_id)
            except Cluster.DoesNotExist:
                logger.error(f"No such cluster: ID={cluster_id}.")
                raise

            runner = ClusterRunner(cluster)
            runner.run()
    except LockError:
        logger.error(f"'{lock_name}' already locked.")


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
