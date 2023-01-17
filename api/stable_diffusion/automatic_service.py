import asyncio
import datetime
import logging
from pathlib import Path
from typing import Optional

from yapapi import Golem
from yapapi.contrib.service.http_proxy import HttpProxyService, LocalHttpProxy
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import Service, ServiceState, Cluster


CLUSTER_INSTANCES_NUMBER = 1
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


class AutomaticService(HttpProxyService):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            # image_hash='2b974c2d48fccd52c4b0d3413b628af30851cd7d2af57eea251b4ef8',
            # image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-diffusers-golem-latest-3b13fd1916.gvmi',
            image_hash='17de6c863581d53355f7cdeb8ec5f6d7eb43604494ea958a9dfe3ef7',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-automatic-golem-latest-7c4666b6aa.gvmi',
            capabilities=['vpn', 'cuda*'],
        )

    async def start(self):
        async for script in super().start():
            yield script
        script = self._ctx.new_script()
        script.run("run_service.sh")
        yield script


async def main(port):
    global cluster

    class ClusterNeedsRestart(Exception):
        pass

    while True:
        try:
            async with Golem(budget=CLUSTER_BUDGET, subnet_tag=CLUSTER_SUBNET_TAG) as golem:
                # network = await golem.create_network("192.168.0.1/24")
                cluster = await golem.run_service(
                    AutomaticService,
                    instance_params=[{"remote_port": port}],
                    # network=network,
                    expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME
                )

                def still_starting():
                    return any(i.state in (ServiceState.pending, ServiceState.starting) for i in cluster.instances)

                while still_starting():
                    print_instances()
                    await asyncio.sleep(5)

                # proxy = LocalHttpProxy(cluster, port)
                # await proxy.run()
                # print(f"Local HTTP server listening on:\nhttp://localhost:{port}")

                while True:
                    await asyncio.sleep(60 * 3)
                    print_instances()
                    instance_to_reset = next((i for i in cluster.instances if i.state == ServiceState.terminated), None)
                    if instance_to_reset is not None:
                        # We must restart cluster. Should not happen often.
                        logger.warning(f'instance was terminated. Restarting Golem cluster')
                        raise ClusterNeedsRestart
        except ClusterNeedsRestart:
            cluster.stop()
        except Exception as e:
            # await proxy.stop()
            print(f"HTTP server stopped")
            cluster.stop()
            # await network.remove()


def print_instances():
    message = f"Cluster instances: " + str([
        f"instance: {s.state.value}" + (f" on {s.provider_name}" if s.provider_id else "")
        for s in cluster.instances
    ])
    logger.info(message)


def run_sd_service():
    try:
        asyncio.run(main(7861))
    except KeyboardInterrupt:
        logger.info('Interruption')
    finally:
        logger.info('Stopping cluster')
        cluster.stop()


if __name__ == "__main__":
    run_sd_service()
