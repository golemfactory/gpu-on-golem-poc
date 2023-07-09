import asyncio
import datetime
import pathlib
import random
import string
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


class ConcreteProviderStrategy(MarketStrategy):
    def __init__(self, provider_id):
        self.provider_id = provider_id

    async def score_offer(self, offer):
        return SCORE_TRUSTED if offer.issuer == self.provider_id else SCORE_REJECTED


class TextUIService(SocketProxyService):
    UI_PORT = 80  # nginx is listening on this port and forwarding to 8000
    TEXT_UI_PORT = 8000  # FE port for text-generation-webui software
    TEXT_UI_API_PORT = 8001  # Blocking API port for text-generation-webui software
    SSH_PORT = 22

    def __init__(self, proxy: SocketProxy):
        super().__init__()
        self.proxy = proxy

    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='54e16c800935e8831adc5b47a89a7d69c8093b861ec4c62c1989a2d6',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/text-webui-golem-54e16c800935e8831adc5b47a89a7d69c8093b861ec4c62c1989a2d6.gvmi',
            capabilities=[vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        # perform the initialization of the Service
        # (which includes sending the network details within the `deploy` command)
        async for script in super().start():
            yield script

        password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        script = self._ctx.new_script(timeout=datetime.timedelta(seconds=300))
        script.run("/bin/bash", "-c", "mkdir /usr/src/app/output/training")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/training/datasets /usr/src/app/output/training/datasets && ln -s /usr/src/app/output/training/datasets /home/python_user/text-generation-webui/training/datasets")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/training/formats /usr/src/app/output/training/formats && ln -s /usr/src/app/output/training/formats /home/python_user/text-generation-webui/training/formats")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/models /usr/src/app/output/models && ln -s /usr/src/app/output/models /home/python_user/text-generation-webui/models")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/loras /usr/src/app/output/loras && ln -s /usr/src/app/output/loras /home/python_user/text-generation-webui/loras")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/prompts /usr/src/app/output/prompts && ln -s /usr/src/app/output/prompts /home/python_user/text-generation-webui/prompts")
        script.run("/bin/bash", "-c", "mv /home/python_user/text-generation-webui/presets /usr/src/app/output/presets && ln -s /usr/src/app/output/presets /home/python_user/text-generation-webui/presets")

        script.run("/bin/bash", "-c", "ssh-keygen -A")
        script.run("/bin/bash", "-c", f'echo -e "{password}\n{password}" | passwd')
        script.run("/bin/bash", "-c", "/usr/sbin/sshd")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/run_service.sh", str(self.TEXT_UI_API_PORT), "127.0.0.1", str(self.TEXT_UI_PORT))
        yield script

        script = self._ctx.new_script()
        script.run("/usr/sbin/nginx")
        yield script

        await self.proxy.run_server(self, self.UI_PORT)
        server = await self.proxy.run_server(self, self.SSH_PORT)

        script = self._ctx.new_script()
        script.run("/usr/src/app/wait_for_service.sh", str(self.TEXT_UI_API_PORT))
        yield script

        with Session(engine) as session:
            offer = session.exec(select(Offer).where(Offer.provider_id == self.provider_id)).one()
            offer.status = OfferStatus.READY
            offer.password = password
            session.add(offer)
            session.commit()

        print(
            f"connect with:\n"
            f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
            f"-p {server.local_port} root@{server.local_address}"
        )
        print(f"password: {password}")


async def main(provider_id: str, webui_port: int, ssh_port: int):
    """
    :param provider_id:
    :param webui_port: The port on requestor to tunnel webui.
    :param ssh_port: The port on requestor to tunnel ssh.
    """

    async with Golem(budget=1.0, subnet_tag='gpu-test', strategy=ConcreteProviderStrategy(provider_id)) as golem:
        network = await golem.create_network("192.168.0.1/24")
        proxy = SocketProxy(address='0.0.0.0', ports=[webui_port, ssh_port])

        async with network:
            cluster = await golem.run_service(
                TextUIService,
                network=network,
                expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME,
                num_instances=1,
                instance_params=[{'proxy': proxy}]
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


def rent_server(provider_id: str, webui_port: int, ssh_port: int):
    try:
        asyncio.run(main(provider_id, webui_port, ssh_port))
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
    rent_server(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
