import logging
import time

from clusters.models import Cluster, Worker


logger = logging.getLogger(__name__)


class ClusterRunner:
    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    def run(self):
        if not self._should_start():
            logger.info(f"Cluster {self.cluster.id} in status: {self.cluster.status}. Not starting.")

        while self._should_run():
            self._workers_healthcheck()
            is_modified = self._adjust_workers()
            if is_modified:
                # TODO: schedule load balacer config refresh task
                pass

            time.sleep(5)
            self.cluster.refresh_from_db()

        self.cluster.status = Cluster.Status.TERMINATED
        self.cluster.save(update_fields=["status"])

    def _should_start(self):
        return self.cluster.status is Cluster.Status.PENDING

    def _should_run(self):
        return self.cluster.status is not Cluster.Status.SHUTTING_DOWN

    def _workers_healthcheck(self):
        # We can check with API of provider and verify with load balancer stats
        # Mark non-responsive workers with status=BAD
        pass

    def _adjust_workers(self) -> bool:
        bad_workers = self.cluster.workers.filter(status=Worker.Status.BAD)
        for bad_worker in bad_workers:
            self._terminate_worker(bad_worker)

        ok_workers = self.cluster.workers.filter(status__in=(Worker.Status.STARTING, Worker.Status.OK))
        ok_workers_count = ok_workers.count()
        delta_workers = self.cluster.size - ok_workers_count
        if delta_workers > 0:
            for _ in range(delta_workers):
                self._start_worker()
        elif delta_workers < 0:
            for redundant_worker in ok_workers[-delta_workers:]:
                self._terminate_worker(redundant_worker)

        is_cluster_modified = len(bad_workers) > 0 or delta_workers > 0
        return is_cluster_modified

    def _start_worker(self):
        # TODO: Start worker using provider API
        pass

    def _terminate_worker(self, worker: Worker):
        # TODO: Terminate worker using provider API
        pass
