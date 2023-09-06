import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Cluster
from clusters.runner import ClusterRunner

from rent_golem.celery import app


logger = logging.getLogger(__name__)

CLUSTER_LOCK_NAME = "CLUSTER_RUN_LOCK_{cluster_id}"
CLUSTER_LOCK_TIMEOUT_SECONDS = 5 * 60


@app.task(bind=True)
def run_cluster(self, cluster_id: str):
    logger.info('Starting run cluster.')
    lock_name = CLUSTER_LOCK_NAME.format(cluster_id=cluster_id)
    try:
        with cache.lock(lock_name, blocking_timeout=0, timeout=CLUSTER_LOCK_TIMEOUT_SECONDS) as cluster_lock:
            logger.info('Lock acquired.')
            try:
                cluster = Cluster.objects.get(pk=cluster_id)
            except Cluster.DoesNotExist:
                logger.error(f"No such cluster: ID={cluster_id}.")
                raise

            runner = ClusterRunner(cluster, cluster_lock)
            runner.run()
    except LockError:
        logger.error(f"'{lock_name}' already locked.")
