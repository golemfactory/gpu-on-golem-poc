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


class NginxService(HttpProxyService):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash="16ad039c00f60a48c76d0644c96ccba63b13296d140477c736512127",
            capabilities=[vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        # perform the initialization of the Service
        # (which includes sending the network details within the `deploy` command)
        async for script in super().start():
            yield script

        # start the remote HTTP server and give it some content to serve in the `index.html`
        script = self._ctx.new_script()
        script.run("/docker-entrypoint.sh")
        script.run("/bin/chmod", "a+x", "/")
        msg = "Hello"
        script.run(
            "/bin/sh",
            "-c",
            f"echo {msg} > /usr/share/nginx/html/index.html",
        )
        script.run("/usr/sbin/nginx"),
        yield script


class AutomaticService(HttpProxyService):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='39600d3ef4f1cd87e4f3f70cd7b91a6dca55ceea9c897c50de76d4d3',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-automatic-golem-test-39600d3ef4f1cd87e4f3f70cd7b91a6dca55ceea9c897c50de76d4d3.gvmi',
            capabilities=[vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        async for script in super().start():
            yield script

        script = self._ctx.new_script()
        script.upload_file('/home/dev/gpu-on-golem-poc/provider/automatic.conf', '/usr/src/app/output/automatic.conf')
        script.run("/usr/bin/cp", "/usr/src/app/output/automatic.conf", "/etc/nginx/conf.d/"),
        yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/run_service_alt.sh", "127.0.0.1", "8000")
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
                    # instance_params=[{"remote_port": 8000}],
                    network=network,
                    expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME
                )
                # cluster = await golem.run_service(
                #     NginxService,
                #     network=network,
                #     expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME
                # )

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
