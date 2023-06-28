import asyncio
import bisect
import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Optional

import sentry_sdk
from yapapi import Golem
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import Service, ServiceState, Cluster

from api.choices import JobStatus
from config import SENTRY_DSN
from redis_db.functions import update_job_data, set_service_data, jobs_queue, set_provider_processing_time


CLUSTER_INSTANCES_NUMBER = os.environ.get('GPUOG_INSTANCES_NUMBER', 1)
CLUSTER_SUBNET_TAG = os.environ.get('GPUOG_SUBNET', 'public')
CLUSTER_BUDGET = 10.0
CLUSTER_EXPIRATION_TIME = datetime.timedelta(days=365)
INTERMEDIARY_IMAGES_NUMBER = 3
# MD5 hash of a black image provided by service when NSFW content is detected
NSFW_IMAGE_HASH = '4518b9ae5041f25d03106e4bb7d019d1'
JOB_EXPIRATION_TIME = datetime.timedelta(hours=1)

sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)
data_dir = Path(os.environ.get("GPUOG_DATA_DIR") or Path(__file__).parent.joinpath('../../api').absolute())
enable_default_logger(log_file=str(data_dir / 'sd-golem-service.log'))
logger = logging.getLogger('yapapi')

cluster: Optional[Cluster] = None


class GenerateImageService(Service):
    def __init__(self, *args, instance_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = instance_name

    @staticmethod
    async def get_payload():
        return await vm.repo(
            # Stable diffusion 1.5
            image_hash='2076c1bfe344fa5248c3c62567cf2484118561f9a48e73460bf7c477',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-txt2img-golem-latest-86465aabf7.gvmi',
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
            await asyncio.sleep(0.3)

            job_started_at = datetime.datetime.now()
            if datetime.datetime.fromtimestamp(job['created_at']) + JOB_EXPIRATION_TIME < job_started_at:
                logger.info(f'{self.name}: job {job["job_id"]} expired. Ignoring.')
                continue

            job_data_update = {
                'status': JobStatus.PROCESSING.value,
                'provider_name': self.provider_name,
                'provider_id': self.provider_id,
                'started_at': job_started_at.isoformat(),
                'queue_position': 0,
                'jobs_in_queue': await jobs_queue.qsize(),
            }
            await update_job_data(job["job_id"], job_data_update)

            logger.info(f'{self.name}: running job for: {job["prompt"]}')

            generate_script = self._ctx.new_script()
            generate_script.run('generate.sh', job["prompt"])
            yield generate_script

            progress = 0
            downloaded_images = set()
            images_to_download = set()
            intermediary_images = []

            while progress < 100:
                await asyncio.sleep(1)

                status_script = self._ctx.new_script()
                future_result = status_script.run("get_status.sh")
                yield status_script
                result = await future_result
                progress_data = json.loads(result.stdout.strip())
                progress = progress_data['progress']
                if 'images' in progress_data and progress_data['images']:
                    images_to_download = set(progress_data['images']) - downloaded_images

                if images_to_download:
                    download_script = self._ctx.new_script()
                    for image in images_to_download:
                        img_filename = image.split('/', 1)[1]
                        img_iteration = img_filename.split('.', 1)[0].split('_', 1)[1]
                        target_filename = f'images/{job["job_id"]}_{img_iteration}.jpg'
                        target_path = str(data_dir / target_filename)
                        download_script.download_file(f'/usr/src/app/output/{img_filename}', target_path)
                        bisect.insort(intermediary_images, target_filename)
                    yield download_script
                    downloaded_images.update(images_to_download)
                    images_to_download.clear()
                if progress < 100:
                    job_data_update = {
                        "status": JobStatus.PROCESSING.value,
                        "progress": progress,
                        "intermediary_images": intermediary_images,
                        'queue_position': 0,
                        "jobs_in_queue": await jobs_queue.qsize(),
                    }
                    await update_job_data(job["job_id"], job_data_update)

            script = self._ctx.new_script()
            final_img_path = str(data_dir / f'images/{job["job_id"]}.jpg')
            script.download_file('/usr/src/app/output/img.jpg', final_img_path)
            logger.info(f'{self.name}: finished job {job["job_id"]} ({job["prompt"]})')
            yield script

            image_blocked = hashlib.md5(open(final_img_path, 'rb').read()).hexdigest() == NSFW_IMAGE_HASH
            final_status = JobStatus.BLOCKED if image_blocked else JobStatus.FINISHED
            job_data_update = {
                "status": final_status.value,
                "ended_at": datetime.datetime.now().isoformat(),
                "progress": progress,
                "processing_time": (datetime.datetime.now() - job_started_at).total_seconds(),
                "img_url": final_img_path,
                "intermediary_images": intermediary_images,
                'queue_position': 0,
                "jobs_in_queue": await jobs_queue.qsize(),
            }
            await update_job_data(job["job_id"], job_data_update)
            await set_provider_processing_time(self.provider_id, job_data_update['processing_time'])


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
                    await set_service_data(prepare_service_data(cluster, golem))
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
            await set_service_data({})


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
        asyncio.run(set_service_data({}))


if __name__ == "__main__":
    run_sd_service()
