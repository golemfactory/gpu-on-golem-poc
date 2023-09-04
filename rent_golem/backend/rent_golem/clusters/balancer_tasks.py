from datetime import timedelta
import logging
from pathlib import Path

from django.core.cache import cache
from redis.exceptions import LockError

from clusters.models import Cluster, Worker
from rent_golem.celery import app

logger = logging.getLogger(__name__)

LOAD_BALANCER_LOCK_NAME = "LOAD_BALANCER_LOCK"
LOAD_BALANCER_LOCK_TIMEOUT = timedelta(seconds=10)
LOAD_BALANCER_CONFIG_TEMPLATE_PATH = Path('/usr/local/etc/haproxy/haproxy.cfg.template')
LOAD_BALANCER_CONFIG_PATH = Path('/usr/local/etc/haproxy/haproxy.cfg')
CONFIG_TEMPLATE = """\
frontend http_{cluster_id}
    bind *:8100
    default_backend be_cluster_{cluster_id}

backend be_cluster_{cluster_id}
    http-send-name-header Host
{workers_section}
"""
CONFIG_WORKER_ENTRY_TEMPLATE = "    server {worker_address} {worker_address}:80 maxconn 1 check"


@app.task(
    bind=True,
    autoretry_for=(LockError,),
    retry_kwargs={'max_retries': 3, 'countdown': 2}
)
def refresh_config(self):
    with cache.lock(
            LOAD_BALANCER_LOCK_NAME,
            blocking_timeout=0,
            timeout=LOAD_BALANCER_LOCK_TIMEOUT.total_seconds()
    ):
        cluster_configs = [
            create_load_balancer_config(cluster)
            for cluster in Cluster.objects.filter(status=Cluster.Status.RUNNING)
        ]
        with LOAD_BALANCER_CONFIG_TEMPLATE_PATH.open('r') as template:
            config_content = template.read()
            config_content += "\n\n".join(cluster_configs)
            with LOAD_BALANCER_CONFIG_PATH.open('w') as balancer_config:
                logger.info(f'Saving load balancer config to file: {LOAD_BALANCER_CONFIG_PATH}. {config_content}')
                # Load balancer container triggers reload when config file is closed after write
                balancer_config.write(config_content)
        logger.debug('Load balancer configuration refreshed.')


def create_load_balancer_config(cluster: Cluster) -> str:
    workers_entries = [
        CONFIG_WORKER_ENTRY_TEMPLATE.format(worker_address=worker.address)
        for worker in cluster.workers.filter(status=Worker.Status.OK)
    ]
    workers_section = '\n'.join(workers_entries)

    return CONFIG_TEMPLATE.format(
        cluster_id=cluster.short_id,
        workers_section=workers_section
    )
