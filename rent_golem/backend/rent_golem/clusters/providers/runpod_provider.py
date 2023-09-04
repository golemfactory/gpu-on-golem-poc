from datetime import datetime, timedelta
import logging
import time

from django.conf import settings
from django.utils import timezone
import requests
from rest_framework import status
import runpod
from runpod.error import QueryError

from clusters.models import Worker

logger = logging.getLogger(__name__)
runpod.api_key = settings.RUNPOD_API_KEY


WORKER_CREATION_TIMEOUT = timedelta(minutes=20)
WORKER_TERMINATION_TIMEOUT = timedelta(seconds=10)
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
        worker.status = Worker.Status.STOPPED
        worker.save(update_fields=['status'])
        return
    else:
        worker.service_id = pod['id']
        worker.address = f"{pod['id']}-8000.proxy.runpod.net"
        worker.save()

    is_running = True
    while is_running and not is_worker_reachable(worker):
        time.sleep(WORKER_STATUS_CHECK_INTERVAL.total_seconds())

        time_elapsed = datetime.now() - creation_time
        if time_elapsed > WORKER_CREATION_TIMEOUT:
            worker.status = Worker.Status.BAD
            worker.save(update_fields=['status'])
            logger.error(f"Worker {worker} creation timed out. Marking as '{Worker.Status.BAD}'.")
            return

        worker_data = runpod.get_pod(pod['id'])
        is_running = worker_data is not None and worker_data['desiredStatus'] == 'RUNNING'
        logger.debug(f'Checking worker {worker} status: {worker_data}.')

    worker.status = Worker.Status.OK if is_running else Worker.Status.STOPPED
    worker.save(update_fields=['status'])
    logger.info(f'Worker {worker} changed status to: {worker.status}.')


def terminate_runpod_worker(worker: Worker):
    if worker.service_id is not None:
        try:
            runpod.terminate_pod(worker.service_id)
        except QueryError as e:
            logger.error(f"Cannot terminate worker: {worker}.", extra={'error': str(e)})
    else:
        logger.warning("Cannot terminate worker on provider side without ID.")

    worker.status = Worker.Status.STOPPED
    worker.save(update_fields=['status'])


def stop_orphaned_runpod_machines():
    """
    Checking if there are any machines working on RUNPOD
    which do not exist in the system or are marked as stopped.
    Alerting and terminating such machines.
    """

    runpod_ids = {pod['id'] for pod in runpod.get_pods()}
    stopped_workers = set(Worker.objects.filter(
        status=Worker.Status.STOPPED,
        last_update__lt=(timezone.now() - WORKER_TERMINATION_TIMEOUT)
    ).values_list('service_id', flat=True))
    all_workers = set(Worker.objects.all().values_list('service_id', flat=True))

    runpod_running_but_marked_as_stopped_in_system = runpod_ids.intersection(stopped_workers)
    if runpod_running_but_marked_as_stopped_in_system:
        logger.warning(f'Detected running RUNPOD workers which should be stopped: '
                       f'{runpod_running_but_marked_as_stopped_in_system}. Stopping...')
        for runpod_id in runpod_running_but_marked_as_stopped_in_system:
            runpod.terminate_pod(runpod_id)

    runpod_running_but_not_exist_in_system = runpod_ids.difference(all_workers)
    if runpod_running_but_not_exist_in_system:
        logger.warning(f'Detected running RUNPOD workers which do not exist in the system: '
                       f'{runpod_running_but_not_exist_in_system}. Stopping...')
        for runpod_id in runpod_running_but_not_exist_in_system:
            runpod.terminate_pod(runpod_id)
