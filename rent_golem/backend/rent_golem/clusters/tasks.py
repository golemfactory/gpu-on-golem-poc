import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Cluster
from clusters.runner import ClusterRunner
from rent_golem.celery import app


logger = logging.getLogger(__name__)

CLUSTER_LOCK_NAME = "CLUSTER_RUN_LOCK_{cluster_id}"


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
