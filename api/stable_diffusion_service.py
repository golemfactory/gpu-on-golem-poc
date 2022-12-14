import asyncio
import datetime
import logging
from typing import Optional

from aioprocessing import AioQueue
from yapapi import Golem
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import Service, ServiceState, Cluster

from redis_functions import publish_job_status, update_job_data, set_service_data


CLUSTER_INSTANCES_NUMBER = 2
CLUSTER_SUBNET_TAG = 'sd-test'
CLUSTER_BUDGET = 10.0
CLUSTER_EXPIRATION_TIME = datetime.timedelta(days=365)

enable_default_logger(log_file="sd-golem-service.log")
logger = logging.getLogger('yapapi')

cluster: Optional[Cluster] = None
q: Optional[AioQueue] = None


class GenerateImageService(Service):
    def __init__(self, *args, instance_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = instance_name

    @staticmethod
    async def get_payload():
        return await vm.repo(
            # VM image placed at private server.
            image_hash='7b4c3af105db6b00b78b57752a0808919755c1f00ae6a78b9b85ffed',
            image_url='http://116.203.41.115:8000/docker-diffusers-golem-latest-3fdf198f2f.gvmi',
        )

    async def start(self):
        async for script in super().start():
            yield script
        script = self._ctx.new_script()
        script.run("run_service.sh")
        yield script

    async def run(self):
        while True:
            logger.info(f"{self.name}: waiting for next job")
            job = await q.coro_get()

            job_data_update = {
                "status": "processing",
                'provider_name': self.provider_name,
                'started_at': datetime.datetime.now().isoformat(),
            }
            await update_job_data(job["job_id"], job_data_update)
            await publish_job_status(job["job_id"], "processing")

            logger.info(f'{self.name}: running job for: {job["prompt"]}')
            script = self._ctx.new_script()
            run_result = script.run('generate.sh', job["prompt"])
            yield script
            await run_result

            script = self._ctx.new_script()
            img_path = f'images/{job["job_id"]}.png'
            script.download_file('/usr/src/app/output/img.png', img_path)
            logger.info(f'{self.name}: finished job {job["job_id"]} ({job["prompt"]})')

            yield script

            job_data_update = {
                "status": "finished",
                "ended_at": datetime.datetime.now().isoformat(),
                "img_url": img_path,
            }
            await update_job_data(job["job_id"], job_data_update)
            await publish_job_status(job["job_id"], "finished")


async def main(num_instances):
    global cluster

    class ClusterNeedsRestart(Exception):
        pass

    while True:
        try:
            async with Golem(budget=CLUSTER_BUDGET, subnet_tag=CLUSTER_SUBNET_TAG) as golem:
                cluster = await golem.run_service(
                    GenerateImageService,
                    instance_params=[{"instance_name": f"sd-service-{i + 1}"} for i in range(num_instances)],
                    expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME
                )

                def still_starting():
                    return any(i.state in (ServiceState.pending, ServiceState.starting) for i in cluster.instances)

                while still_starting():
                    print_instances()
                    await asyncio.sleep(5)

                while True:
                    await asyncio.sleep(60 * 3)
                    print_instances()
                    await set_service_data(prepare_service_data(cluster, golem))
                    instance_to_reset = next((i for i in cluster.instances if i.state == ServiceState.terminated), None)
                    if instance_to_reset is not None:
                        # We must restart cluster. Should not happen often.
                        logger.warning(f'{instance_to_reset.name} was terminated. Restarting Golem cluster')
                        raise ClusterNeedsRestart
        except ClusterNeedsRestart:
            cluster.stop()


def prepare_service_data(current_cluster: Cluster, golem: Golem) -> dict:
    return {
        'golem': {
            'operative': golem.operative, 'payment_driver': golem.payment_driver,
            'payment_network': golem.payment_network,
        },
        'cluster': {
            'expiration': current_cluster.expiration.isoformat(timespec='seconds'),
            'payload': {
                'image_hash': current_cluster.payload.image_hash, 'image_url': current_cluster.payload.image_url,
            },
            'instances': [
                {
                    'name': i.name,
                    'provider_name': i.provider_name,
                    'provider_id': i.provider_id,
                    'state': i.state.name,
                }
                for i in current_cluster.instances
            ]
        }
    }


def print_instances():
    message = f"Cluster instances: " + str([
        f"{s.name}: {s.state.value}" + (f" on {s.provider_name}" if s.provider_id else "")
        for s in cluster.instances
    ])
    logger.info(message)


def run_sd_service(main_process_queue):
    global q
    q = main_process_queue
    try:
        asyncio.run(main(CLUSTER_INSTANCES_NUMBER))
    except KeyboardInterrupt:
        logger.info('Interruption')
    finally:
        logger.info('Stopping cluster')
        cluster.stop()
