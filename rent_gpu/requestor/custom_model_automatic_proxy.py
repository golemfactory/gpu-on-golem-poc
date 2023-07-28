import asyncio
import base64
import datetime
import pathlib
import sys

from sqlmodel import Session, select
from yapapi import Golem
from yapapi.contrib.service.socket_proxy import SocketProxy, SocketProxyService
from yapapi.payload import vm
from yapapi.services import ServiceState
from yapapi.strategy import SCORE_REJECTED, SCORE_TRUSTED, MarketStrategy

from rent_gpu.requestor.db import engine, Offer, OfferStatus, MACHINE_LIFETIME


CLUSTER_EXPIRATION_TIME = datetime.timedelta(days=365)

examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))

IMAGE_URL = 'http://gpu-on-golem.s3.eu-central-1.amazonaws.com/automatic-golem-custom-model-0cd20b493fe3b8593586913cd47ff1f74b421e47558896ab17c17282.gvmi'
IMAGE_HASH = '0cd20b493fe3b8593586913cd47ff1f74b421e47558896ab17c17282'


class ConcreteProviderStrategy(MarketStrategy):
    def __init__(self, provider_id):
        self.provider_id = provider_id

    async def score_offer(self, offer):
        return SCORE_TRUSTED if offer.issuer == self.provider_id else SCORE_REJECTED


class AutomaticService(SocketProxyService):
    UI_PORT = 80  # nginx is listening on this port and forwarding to SD_UI_PORT
    SD_UI_PORT = 8000  # FE port for stable-diffusion-webui software

    def __init__(self, proxy: SocketProxy, hf_username, hf_password, model_url):
        super().__init__()
        self.proxy = proxy
        self.hf_username = hf_username
        self.hf_password = hf_password
        self.model_url = model_url

    @staticmethod
    async def get_payload():
        manifest = open(pathlib.Path(__file__).parent.joinpath("custom_model_manifest.json"), "rb").read()
        manifest = (manifest
                    .decode('utf-8')
                    .replace('{sha3}', IMAGE_HASH)
                    .replace('{image_url}', IMAGE_URL))
        manifest = base64.b64encode(manifest.encode('utf-8')).decode("utf-8")

        return await vm.manifest(
            manifest=manifest,
            capabilities=["inet", "manifest-support", vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        # perform the initialization of the Service
        # (which includes sending the network details within the `deploy` command)
        async for script in super().start():
            yield script

        script = self._ctx.new_script()
        script.run("/bin/bash", "-c",
                   'mv /usr/src/app/stable-diffusion-webui/models /usr/src/app/output/models && ln -s /usr/src/app/output/models /usr/src/app/stable-diffusion-webui/models')
        yield script

        script = self._ctx.new_script()
        script.run("/bin/bash", "-c", 'echo "108.138.51.21 huggingface.co" >> /etc/hosts')
        script.run("/bin/bash", "-c", 'echo "18.244.102.9 cdn-lfs.huggingface.co" >> /etc/hosts')
        yield script

        # This is making sure that outbound interface has proper MTU
        # There was problem with too big MTU resulting in permanent lost packets
        script = self._ctx.new_script()
        script.run('/sbin/ifconfig', 'eth1', 'mtu', '1450', 'up'),
        yield script

        credentials = f'-u {self.hf_username}:{self.hf_password}' if self.hf_username and self.hf_password else ''
        script = self._ctx.new_script()
        script.run("/bin/bash", "-c", f"cd /usr/src/app/output/models/Stable-diffusion && curl -L --remote-name --remote-header-name {credentials} {self.model_url}")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/run_service.sh", "127.0.0.1", str(self.SD_UI_PORT))
        yield script

        script = self._ctx.new_script()
        script.run("/usr/sbin/nginx")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/wait_for_service.sh", str(self.SD_UI_PORT))
        yield script

        await self.proxy.run_server(self, self.UI_PORT)

        with Session(engine) as session:
            offer = session.exec(select(Offer).where(Offer.provider_id == self.provider_id)).one()
            offer.status = OfferStatus.READY
            session.add(offer)
            session.commit()


async def main(provider_id: str, local_port: int, model_url: str, hf_username: str, hf_password: str):
    """
    :param provider_id:
    :param local_port: The port on requestor through which tunnel is opened to provider machine.
    """

    async with Golem(budget=1.0, subnet_tag='gpu-test', strategy=ConcreteProviderStrategy(provider_id)) as golem:
        network = await golem.create_network("192.168.0.1/24")
        proxy = SocketProxy(address='0.0.0.0', ports=[local_port])

        async with network:
            cluster = await golem.run_service(
                AutomaticService,
                network=network,
                expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME,
                num_instances=1,
                instance_params=[{"proxy": proxy, "hf_username": hf_username, "hf_password": hf_password, "model_url": model_url}],
            )
            instances = cluster.instances

            def still_starting():
                return any(i.state in (ServiceState.pending, ServiceState.starting) for i in instances)

            while still_starting():
                print('Starting')
                await asyncio.sleep(5)

            while True:
                print(instances)
                try:
                    await asyncio.sleep(5)
                    with Session(engine) as session:
                        offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
                        if offer.started_at and datetime.datetime.now() > offer.started_at + MACHINE_LIFETIME:
                            offer.status = OfferStatus.TERMINATING
                            session.add(offer)
                            session.commit()
                        if offer.status == OfferStatus.TERMINATING:
                            break
                except (KeyboardInterrupt, asyncio.CancelledError):
                    break

            await proxy.stop()
            cluster.stop()

            cnt = 0
            while cnt < 3 and any(s.is_available for s in instances):
                print(instances)
                await asyncio.sleep(5)
                cnt += 1


def rent_server(provider_id: str, local_port: int, model_url: str, hf_username: str = None, hf_password: str = None):
    try:
        asyncio.run(main(provider_id, local_port, model_url, hf_username, hf_password))
    except KeyboardInterrupt:
        print('Interruption')
    finally:
        with Session(engine) as session:
            offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
            offer.status = OfferStatus.FREE
            offer.port = None
            offer.password = None
            offer.started_at = None
            offer.job_id = None
            offer.package = None
            offer.reserved_by = None
            session.add(offer)
            session.commit()


if __name__ == "__main__":
    user = sys.argv[4] if len(sys.argv) > 5 else None
    password = sys.argv[5] if len(sys.argv) > 5 else None
    rent_server(sys.argv[1], int(sys.argv[2]), sys.argv[3], user, password)
