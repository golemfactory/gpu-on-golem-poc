from datetime import timedelta
import logging
import time
from typing import List

from celery import chord
from redis.lock import Lock

from clusters.models import Cluster, Worker, Provider
from clusters.worker_tasks import create_worker, terminate_worker, check_worker_health
from clusters.balancer_tasks import refresh_config


logger = logging.getLogger(__name__)
WORKERS_HEALTHCHECK_INTERVAL = timedelta(seconds=5)


class ClusterRunner:
    def __init__(self, cluster: Cluster, cluster_lock: Lock):
        self.cluster = cluster
        # Since clusters should run correctly for multiple days,
        # we keep reference to lock to prolong it while runner is working correctly.
        self.cluster_lock = cluster_lock

    def run(self):
        if not self._should_start():
            logger.info(f"Cluster {self.cluster.pk} in status: {self.cluster.status}. Not starting.")
            return

        while self._should_run():
            any_worker_status_changed = self._workers_healthcheck()
            self._update_cluster_status()
            self._terminate_bad_workers()

            logger.debug(f'Any worker status changed: {any_worker_status_changed}.')
            if any_worker_status_changed:
                refresh_config.delay()

            self._adjust_cluster_size()

            time.sleep(WORKERS_HEALTHCHECK_INTERVAL.total_seconds())
            self.cluster.refresh_from_db()
            # Reset lock timeout infinitely while this process is running
            self.cluster_lock.reacquire()

        logger.debug(f"Terminating cluster: {self.cluster}.")
        self._terminate_cluster()

    def _should_start(self):
        return self.cluster.status == Cluster.Status.PENDING

    def _should_run(self):
        if self.cluster.status == Cluster.Status.TERMINATED:
            logger.warning(f"Running Cluster {self.cluster} in {Cluster.Status.TERMINATED} status. Should not happen.")
            return False
        else:
            return self.cluster.status != Cluster.Status.SHUTTING_DOWN

    def _workers_healthcheck(self) -> bool:
        logger.debug(f"Running workers healthcheck for cluster: {self.cluster}.")
        status_modifications = [
            check_worker_health(worker)
            for worker in self.cluster.workers.filter(status=Worker.Status.OK)
        ]
        return any(status_modifications)

    def _update_cluster_status(self):
        """
        Cluster starts with status: Status.Pending.
        Status should change to Status.RUNNING if there's at least one worker in OK state.
        It might become Status.PENDING again if there are no OK workers.

        Status.SHUTTING_DOWN is set externally e.x. via API.
        Status.TERMINATED is set after ClusterRunner scheduled all workers to terminate.
        """

        ok_workers = self.cluster.workers.filter(status=Worker.Status.OK)
        new_status = None

        if self.cluster.status == Cluster.Status.PENDING and ok_workers.count() > 0:
            new_status = Cluster.Status.RUNNING
        elif self.cluster.status == Cluster.Status.RUNNING and ok_workers.count() == 0:
            new_status = Cluster.Status.PENDING

        if new_status:
            self.cluster.status = new_status
            self.cluster.save(update_fields=['status'])

    def _adjust_cluster_size(self) -> bool:
        ok_workers = self.cluster.workers.filter(status__in=(Worker.Status.STARTING, Worker.Status.OK))
        ok_workers_count = ok_workers.count()
        delta_workers = self.cluster.size - ok_workers_count
        logger.debug(f"OK or STARTING workers: {ok_workers_count}, Cluster size: {self.cluster.size}, Delta: {delta_workers}.")
        if delta_workers > 0:
            for _ in range(delta_workers):
                self._start_worker()
        elif delta_workers < 0:
            redundant_workers = ok_workers[-delta_workers:]
            self._terminate_workers(redundant_workers)

        is_cluster_modified = delta_workers > 0
        return is_cluster_modified

    def _terminate_bad_workers(self):
        bad_workers = self.cluster.workers.filter(status=Worker.Status.BAD)
        logger.debug(f"Got {len(bad_workers)} bad workers.")
        self._terminate_workers(bad_workers)

    def _start_worker(self):
        worker = Worker.objects.create(
            cluster=self.cluster,
            provider=Provider.RUNPOD,
        )
        create_worker.apply_async((worker.id, ), link=refresh_config.si())

    def _terminate_workers(self, workers: List[Worker]):
        if len(workers) > 0:
            terminate_tasks = [terminate_worker.si(worker.id) for worker in workers]
            # Waiting for termination tasks to finish and then refreshing LB config
            chord(terminate_tasks)(refresh_config.si())

    def _terminate_cluster(self):
        running_workers = self.cluster.workers.exclude(status=Worker.Status.STOPPED)
        self._terminate_workers(running_workers)
        self.cluster.status = Cluster.Status.TERMINATED
        self.cluster.save(update_fields=["status"])
