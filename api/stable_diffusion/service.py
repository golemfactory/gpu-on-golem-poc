import asyncio
import bisect
import datetime
import hashlib
import logging
from pathlib import Path
from typing import Optional

from yapapi import Golem
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import Service, ServiceState, Cluster

from api.choices import JobStatus
from api.redis_functions import (publish_job_status, update_job_data, set_service_data, jobs_queue,
                                 set_provider_processing_time)


CLUSTER_INSTANCES_NUMBER = 2
CLUSTER_SUBNET_TAG = 'public'
CLUSTER_BUDGET = 10.0
CLUSTER_EXPIRATION_TIME = datetime.timedelta(days=365)
INTERMEDIARY_IMAGES_NUMBER = 5
# MD5 hash of a black image provided by service when NSFW content is detected
NSFW_IMAGE_HASH = '62640df3608f0287d980794d720bff31'

api_dir = Path(__file__).parent.joinpath('..').absolute()
enable_default_logger(log_file=str(api_dir / 'sd-golem-service.log'))
logger = logging.getLogger('yapapi')

cluster: Optional[Cluster] = None


class GenerateImageService(Service):
    def __init__(self, *args, instance_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = instance_name

    @staticmethod
    async def get_payload():
        return await vm.repo(
            # Stable diffusion 2.1
            # image_hash='efad0714a2a76eed7a6f250163b73423c5cbe073a8a25f2bbb418e09',
            # image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-diffusers-golem-latest-6cbbba62e8.gvmi',

            # Stable diffusion 1.5
            image_hash='2b974c2d48fccd52c4b0d3413b628af30851cd7d2af57eea251b4ef8',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-diffusers-golem-latest-3b13fd1916.gvmi',

            capabilities=['vpn', 'cuda*'],
        )

    async def start(self):
        async for script in super().start():
            yield script
        script = self._ctx.new_script()
        script.run("run_service.sh", str(INTERMEDIARY_IMAGES_NUMBER))
        yield script

    async def run(self):
        while True:
            logger.info(f"{self.name}: waiting for next job")
            job = await jobs_queue.get()
            await jobs_queue.notify_queued()

            job_started_at = datetime.datetime.now()
            job_data_update = {
                'status': JobStatus.PROCESSING.value,
                'provider_name': self.provider_name,
                'started_at': job_started_at.isoformat(),
            }
            await update_job_data(job["job_id"], job_data_update)
            await publish_job_status(job["job_id"], JobStatus.PROCESSING.value, provider=self.provider_name)

            logger.info(f'{self.name}: running job for: {job["prompt"]}')

            generate_script = self._ctx.new_script()
            generate_script.run('generate.sh', job["prompt"])
            yield generate_script

            progress = 0
            downloaded_images = set()
            images_to_download = set()
            intermediary_images = []

            async def update_progress_data(progress_data: dict):
                nonlocal progress, images_to_download
                progress = progress_data['progress']
                if 'images' in progress_data and progress_data['images']:
                    images_to_download = set(progress_data['images']) - downloaded_images

            while progress < 100:
                await asyncio.sleep(1)
                status_script = self._ctx.new_script()
                status_script.download_json('/usr/src/app/output/status.json', update_progress_data)
                yield status_script
                if images_to_download:
                    download_script = self._ctx.new_script()
                    for image in images_to_download:
                        img_filename = image.split('/', 1)[1]
                        img_iteration = img_filename.split('.', 1)[0].split('_', 1)[1]
                        target_filename = f'images/{job["job_id"]}_{img_iteration}.jpg'
                        target_path = str(api_dir / target_filename)
                        download_script.download_file(f'/usr/src/app/output/{img_filename}', target_path)
                        bisect.insort(intermediary_images, target_filename)
                    yield download_script
                    downloaded_images.update(images_to_download)
                    images_to_download.clear()
                if progress < 100:
                    await publish_job_status(job["job_id"], JobStatus.PROCESSING.value, progress, intermediary_images,
                                             provider=self.provider_name)

            script = self._ctx.new_script()
            final_img_path = str(api_dir / f'images/{job["job_id"]}.png')
            script.download_file('/usr/src/app/output/img.png', final_img_path)
            logger.info(f'{self.name}: finished job {job["job_id"]} ({job["prompt"]})')
            yield script

            image_blocked = hashlib.md5(open(final_img_path, 'rb').read()).hexdigest() == NSFW_IMAGE_HASH
            final_status = JobStatus.BLOCKED if image_blocked else JobStatus.FINISHED
            job_data_update = {
                "status": final_status.value,
                "ended_at": datetime.datetime.now().isoformat(),
                "processing_time": (datetime.datetime.now() - job_started_at).total_seconds(),
                "img_url": final_img_path,
                "intermediary_images": intermediary_images,
            }
            await update_job_data(job["job_id"], job_data_update)
            await publish_job_status(job["job_id"], final_status.value, progress, intermediary_images,
                                     provider=self.provider_name)
            await set_provider_processing_time(self.provider_name, job_data_update['processing_time'])


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
                    print_instances()
                    await set_service_data(prepare_service_data(cluster, golem))
                    await asyncio.sleep(60 * 3)
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
            'operative': golem.operative,
            'payment_driver': golem.payment_driver,
            'payment_network': golem.payment_network,
        },
        'cluster': {
            'expiration': current_cluster.expiration.isoformat(timespec='seconds'),
            'payload': {
                'image_hash': current_cluster.payload.image_hash,
                'image_url': current_cluster.payload.image_url,
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
        },
        'last_update': datetime.datetime.now().isoformat(),
    }


def print_instances():
    message = f"Cluster instances: " + str([
        f"{s.name}: {s.state.value}" + (f" on {s.provider_name}" if s.provider_id else "")
        for s in cluster.instances
    ])
    logger.info(message)


def run_sd_service():
    try:
        asyncio.run(main(CLUSTER_INSTANCES_NUMBER))
    except KeyboardInterrupt:
        logger.info('Interruption')
    finally:
        logger.info('Stopping cluster')
        cluster.stop()


if __name__ == "__main__":
    run_sd_service()
