import asyncio
from datetime import datetime, timedelta
import pathlib
import random
import string
import sys

from sqlmodel import Session, select
from yapapi import Golem
from yapapi.contrib.service.socket_proxy import SocketProxy, SocketProxyService
from yapapi.payload import vm
from yapapi.strategy import SCORE_REJECTED, SCORE_TRUSTED, MarketStrategy

from rent_gpu.requestor.db import engine, Offer, OfferStatus, MACHINE_LIFETIME


examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


class ConcreteProviderStrategy(MarketStrategy):
    def __init__(self, provider_id):
        self.provider_id = provider_id

    async def score_offer(self, offer):
        return SCORE_TRUSTED if offer.issuer == self.provider_id else SCORE_REJECTED


class SshService(SocketProxyService):
    remote_port = 22

    def __init__(self, proxy: SocketProxy):
        super().__init__()
        self.proxy = proxy

    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='856a5ed05eb3055e2b130a44e104d2f34f0a28fa8fa5ae7a958f9cea',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/rent_gpu-856a5ed05eb3055e2b130a44e104d2f34f0a28fa8fa5ae7a958f9cea.gvmi',
            capabilities=[vm.VM_CAPS_VPN],
        )

    async def start(self):
        # perform the initialization of the Service
        # (which includes sending the network details within the `deploy` command)
        async for script in super().start():
            yield script

        password = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

        script = self._ctx.new_script(timeout=timedelta(seconds=10))
        script.run("/bin/bash", "-c", "ssh-keygen -A")
        script.run("/bin/bash", "-c", f'echo -e "{password}\n{password}" | passwd')
        script.run("/bin/bash", "-c", "/usr/sbin/sshd")
        yield script

        server = await self.proxy.run_server(self, self.remote_port)

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


async def main(provider_id: str, local_port: int):
    """
    :param provider_id:
    :param local_port: The port on requestor through which tunnel is opened to provider machine.
    """

    async with Golem(budget=1.0, subnet_tag='gpu-test', strategy=ConcreteProviderStrategy(provider_id)) as golem:

        network = await golem.create_network("192.168.0.1/24")
        proxy = SocketProxy(address='0.0.0.0', ports=[local_port])

        async with network:
            cluster = await golem.run_service(
                SshService,
                network=network,
                num_instances=1,
                instance_params=[{"proxy": proxy}],
            )
            instances = cluster.instances

            while True:
                print(instances)
                try:
                    await asyncio.sleep(5)
                    with Session(engine) as session:
                        offer = session.exec(select(Offer).where(Offer.provider_id == provider_id)).one()
                        if offer.started_at and datetime.now() > offer.started_at + MACHINE_LIFETIME:
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


def rent_server(provider_id: str, local_port: int):
    try:
        asyncio.run(main(provider_id, local_port))
    except KeyboardInterrupt:
        print('Interruption')


if __name__ == "__main__":
    rent_server(sys.argv[1], int(sys.argv[2]))
