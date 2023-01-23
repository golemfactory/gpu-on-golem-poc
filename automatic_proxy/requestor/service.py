import asyncio
import datetime
import logging
from pathlib import Path
from typing import Optional

from yapapi import Golem
from yapapi.contrib.service.http_proxy import HttpProxyService, LocalHttpProxy
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import ServiceState, Cluster


CLUSTER_INSTANCES_NUMBER = 1
CLUSTER_SUBNET_TAG = 'public'
CLUSTER_BUDGET = 10.0
CLUSTER_EXPIRATION_TIME = datetime.timedelta(days=365)
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
            image_hash='2e0c2ebf653707ba1c6cc1ae2beff0a35fe303b4d81b079eda776d34',
            image_url='http://storage.googleapis.com/sd-golem-images/docker-automatic-golem-latest-9aafc23d77.gvmi',
            capabilities=[vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        async for script in super().start():
            yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/run_service.sh", "127.0.0.1", "8000")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/sbin/nginx")
        yield script


async def main(port):
    global cluster

    class ClusterNeedsRestart(Exception):
        pass

    while True:
        try:
            async with Golem(budget=CLUSTER_BUDGET, subnet_tag=CLUSTER_SUBNET_TAG) as golem:
                network = await golem.create_network("192.168.0.1/24")

                cluster = await golem.run_service(
                    AutomaticService,
                    network=network,
                    expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME
                )

                def still_starting():
                    return any(i.state in (ServiceState.pending, ServiceState.starting) for i in cluster.instances)

                while still_starting():
                    print_instances()
                    await asyncio.sleep(5)

                proxy = LocalHttpProxy(cluster, port)
                await proxy.run()
                print(f"Local HTTP server listening on:\nhttp://localhost:{port}")

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
            await proxy.stop()
            print(f"HTTP server stopped")
            cluster.stop()
            await network.remove()


def print_instances():
    message = f"Cluster instances: " + str([
        f"instance: {s.state.value}" + (f" on {s.provider_name}" if s.provider_id else "")
        for s in cluster.instances
    ])
    logger.info(message)


def run_sd_service():
    try:
        asyncio.run(main(8000))
    except KeyboardInterrupt:
        logger.info('Interruption')
    finally:
        logger.info('Stopping cluster')
        cluster.stop()


if __name__ == "__main__":
    run_sd_service()
