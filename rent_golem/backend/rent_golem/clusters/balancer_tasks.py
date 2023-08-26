import logging

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Cluster
from rent_golem.celery import app

LOAD_BALANCER_LOCK_NAME = "LOAD_BALANCER_LOCK"


logger = logging.getLogger(__name__)

@app.task(bind=True)
def refresh_config(self):
    try:
        with cache.lock(LOAD_BALANCER_LOCK_NAME, blocking_timeout=0):
            # TODO
            logger.debug('Refreshing load balancer configuration.')
    except LockError:
        logger.error(f"'{LOAD_BALANCER_LOCK_NAME}' already locked.")
