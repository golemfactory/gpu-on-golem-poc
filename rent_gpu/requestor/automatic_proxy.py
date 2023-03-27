import asyncio
import datetime
import pathlib
import sys

from sqlmodel import Session, select
from yapapi import Golem
from yapapi.contrib.service.http_proxy import HttpProxyService, LocalHttpProxy
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


class AutomaticService(HttpProxyService):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='ca042dce3683749b313c01769d2b8c93545df18fe8a941ca5f67e298',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/automatic-golem-ca042dce3683749b313c01769d2b8c93545df18fe8a941ca5f67e298.gvmi',
            capabilities=[vm.VM_CAPS_VPN, 'cuda*'],
        )

    async def start(self):
        # perform the initialization of the Service
        # (which includes sending the network details within the `deploy` command)
        async for script in super().start():
            yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/run_service.sh", "127.0.0.1", "8000")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/sbin/nginx")
        yield script

        script = self._ctx.new_script()
        script.run("/usr/src/app/wait_for_service.sh", "8000")
        yield script

        with Session(engine) as session:
            offer = session.exec(select(Offer).where(Offer.provider_id == self.provider_id)).one()
            offer.status = OfferStatus.READY
            session.add(offer)
            session.commit()


async def main(provider_id: str, local_port: int):
    """
    :param provider_id:
    :param local_port: The port on requestor through which tunnel is opened to provider machine.
    """

    async with Golem(budget=1.0, subnet_tag='gpu-test', strategy=ConcreteProviderStrategy(provider_id)) as golem:
        network = await golem.create_network("192.168.0.1/24")

        async with network:
            cluster = await golem.run_service(
                AutomaticService,
                network=network,
                expiration=datetime.datetime.now() + CLUSTER_EXPIRATION_TIME,
                num_instances=1,
            )
            instances = cluster.instances

            def still_starting():
                return any(i.state in (ServiceState.pending, ServiceState.starting) for i in instances)

            while still_starting():
                print('Starting')
                await asyncio.sleep(5)

            proxy = LocalHttpProxy(cluster, local_port)
            await proxy.run()

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
