import logging
import time

from clusters.models import Cluster, Worker, Provider
from clusters.tasks import create_worker, terminate_worker


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

        self._terminate_cluster()


    def _should_start(self):
        return self.cluster.status is Cluster.Status.PENDING

    def _should_run(self):
        return self.cluster.status is not Cluster.Status.SHUTTING_DOWN

    def _workers_healthcheck(self):
        # TODO
        # We can check with API of provider and verify with load balancer stats
        # Mark non-responsive workers with status=BAD

        # When in status STARTING then wait for some time before marking as BAD.
        # It would be good to have one place for this in logic for healthcheck and for starting process.
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
        if self.cluster.package_type in (Cluster.Package.AUTOMATIC, Cluster.Package.CUSTOM_AUTOMATIC):
            # This should be probably moved to some other place where settings or code around packages lay.
            # TODO: might be not saved to DB but taken dynamically in code based on worker.cluster.package_type
            healthcheck_path = "/sdapi/v1/sd-models"
        else:
            logger.warning(f"Could not determine healthcheck path for package: {self.cluster.package_type}.")
            healthcheck_path = None

        worker = Worker.objects.create(
            cluster=self.cluster,
            provider=Provider.RUNPOD,
            healthcheck_path=healthcheck_path
        )
        create_worker.delay(worker.id)

    def _terminate_worker(self, worker: Worker):
        terminate_worker.delay(worker.id)

    def _terminate_cluster(self):
        for worker in self.cluster.workers.exclude(status=Worker.Status.STOPPED):
            self._terminate_worker(worker)
        self.cluster.status = Cluster.Status.TERMINATED
        self.cluster.save(update_fields=["status"])
