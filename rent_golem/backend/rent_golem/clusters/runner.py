from datetime import timedelta
import logging
import time

from clusters.models import Cluster, Worker, Provider
from clusters.worker_tasks import create_worker, terminate_worker, check_worker_health
from clusters.balancer_tasks import refresh_config


logger = logging.getLogger(__name__)
WORKERS_HEALTHCHECK_INTERVAL = timedelta(seconds=5)


class ClusterRunner:
    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    def run(self):
        if not self._should_start():
            logger.info(f"Cluster {self.cluster.pk} in status: {self.cluster.status}. Not starting.")

        while self._should_run():
            self._workers_healthcheck()

            is_modified = self._adjust_workers()
            if is_modified:
                refresh_config.delay()

            time.sleep(WORKERS_HEALTHCHECK_INTERVAL.total_seconds())
            self.cluster.refresh_from_db()

        logger.debug(f"Terminating cluster: {self.cluster}.")
        self._terminate_cluster()

    def _should_start(self):
        return self.cluster.status is Cluster.Status.PENDING

    def _should_run(self):
        return self.cluster.status is not Cluster.Status.SHUTTING_DOWN

    def _workers_healthcheck(self):
        logger.debug(f"Running workers healthcheck for cluster: {self.cluster}.")
        for worker in self.cluster.workers.filter(status=Worker.Status.OK):
            check_worker_health(worker)

    def _adjust_workers(self) -> bool:
        bad_workers = self.cluster.workers.filter(status=Worker.Status.BAD)
        logger.debug(f"Got {len(bad_workers)} bad workers.")
        for bad_worker in bad_workers:
            self._terminate_worker(bad_worker)

        ok_workers = self.cluster.workers.filter(status__in=(Worker.Status.STARTING, Worker.Status.OK))
        ok_workers_count = ok_workers.count()
        delta_workers = self.cluster.size - ok_workers_count
        logger.debug(f"Ok workers: {ok_workers_count}, Cluster size: {self.cluster.size}, Delta: {delta_workers}.")
        if delta_workers > 0:
            for _ in range(delta_workers):
                self._start_worker()
        elif delta_workers < 0:
            for redundant_worker in ok_workers[-delta_workers:]:
                self._terminate_worker(redundant_worker)

        is_cluster_modified = len(bad_workers) > 0 or delta_workers > 0
        return is_cluster_modified

    def _start_worker(self):
        worker = Worker.objects.create(
            cluster=self.cluster,
            provider=Provider.RUNPOD,
        )
        create_worker.delay(worker.id)

    def _terminate_worker(self, worker: Worker):
        terminate_worker.delay(worker.id)

    def _terminate_cluster(self):
        for worker in self.cluster.workers.exclude(status=Worker.Status.STOPPED):
            self._terminate_worker(worker)
        self.cluster.status = Cluster.Status.TERMINATED
        self.cluster.save(update_fields=["status"])
