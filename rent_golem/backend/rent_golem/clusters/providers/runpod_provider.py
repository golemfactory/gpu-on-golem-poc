from datetime import datetime, timedelta
import logging
import time

from django.conf import settings
import requests
from rest_framework import status
import runpod
from runpod.error import QueryError

from clusters.models import Worker

logger = logging.getLogger(__name__)
runpod.api_key = settings.RUNPOD_API_KEY


WORKER_CREATION_TIMEOUT = timedelta(minutes=20)
WORKER_STATUS_CHECK_INTERVAL = timedelta(seconds=20)


def worker_exists(worker: Worker) -> bool:
    pod = runpod.get_pod(worker.service_id)
    if pod is None:
        return False
    else:
        return True


def is_worker_reachable(worker: Worker) -> bool:
    response = requests.get(worker.healthcheck_url)
    return response.status_code == status.HTTP_200_OK


def create_runpod_worker(worker: Worker):
    worker_name = f"cluster_{worker.cluster.pk}_worker_{worker.id}"
    try:
        pod = runpod.create_pod(
            worker_name,
            'stan7123/automatic-sd:latest',
            'NVIDIA RTX A5000',
            container_disk_in_gb=20,
            min_memory_in_gb=16,
            docker_args="bash -c '/usr/src/app/start.sh'",
            ports="8000/http"
        )
        creation_time = datetime.now()
    except QueryError as e:
        logger.error(f"Cannot create worker: {worker}.", extra={'error': str(e)})
        return
    else:
        worker.service_id = pod['id']
        worker.address = f"https://{pod['id']}-8000.proxy.runpod.net"
        worker.save()

    worker_data = runpod.get_pod(pod['id'])
    while worker_data['desiredStatus'] == 'RUNNING' and not is_worker_reachable(worker):
        time.sleep(WORKER_STATUS_CHECK_INTERVAL.total_seconds())

        time_elapsed = datetime.now() - creation_time
        if time_elapsed > WORKER_CREATION_TIMEOUT:
            worker.status = Worker.Status.BAD
            worker.save(update_fields=['status'])
            logger.error(f"Worker {worker} creation timed out. Marking as '{Worker.Status.BAD}'.")
            return

        worker_data = runpod.get_pod(pod['id'])
        logger.debug(f'Checking worker {worker} status: {worker_data}.')

    worker.status = Worker.Status.OK
    worker.save(update_fields=['status'])
    logger.info(f'Worker {worker} started.')


def terminate_runpod_worker(worker: Worker):
    assert worker.service_id is not None, "Cannot terminate worker without ID."

    try:
        runpod.terminate_pod(worker.service_id)
    except QueryError as e:
        logger.error(f"Cannot terminate worker: {worker}.", extra={'error': str(e)})
        return
    else:
        worker.status = Worker.Status.STOPPED
        worker.save(update_fields=['status'])
