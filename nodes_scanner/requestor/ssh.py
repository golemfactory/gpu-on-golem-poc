import asyncio
from datetime import datetime, timedelta
import pathlib
import random
import string
import sys

from yapapi import Golem
from yapapi.contrib.service.socket_proxy import SocketProxy, SocketProxyService
from yapapi.payload import vm
from yapapi.strategy import SCORE_REJECTED, SCORE_TRUSTED, MarketStrategy


examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


class ConcreteProviderStrategy(MarketStrategy):
    def __init__(self, provider_id):
        self.provider_id = provider_id

    async def score_offer(self, offer):
        # print(f'Provider selected: {self.provider_id}. Type: {type(self.provider_id)}')
        # print(f'Checking offer from: {offer.issuer}. Type: {type(offer.issuer)}')
        # res = SCORE_TRUSTED if offer.issuer == self.provider_id else SCORE_REJECTED
        # print(f'ACCEPTED?: {res}')
        return SCORE_TRUSTED if offer.issuer == self.provider_id else SCORE_REJECTED


class SshService(SocketProxyService):
    remote_port = 22

    def __init__(self, proxy: SocketProxy):
        super().__init__()
        self.proxy = proxy

    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='f0399956776115ac0988fd96844c1da729e7415e75fef740f013adf7',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/golem_cuda_base-f0399956776115ac0988fd96844c1da729e7415e75fef740f013adf7.gvmi',
            # image_hash = 'd9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff',
            # image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/golem_cuda_base-d9981476ceecb823bfc3b076f93c65eea608e19dce306b6dc1f6a0ff.gvmi',
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

        print(
            f"connect with:\n"
            f"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
            f"-p {server.local_port} root@{server.local_address}"
        )
        print(f"password: {password}")
        # TODO: test file transfer with SCP


async def main(provider_id):
    # By passing `event_consumer=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Golem(budget=1.0, subnet_tag='test', strategy=ConcreteProviderStrategy(provider_id)) as golem:

        network = await golem.create_network("192.168.0.1/24")
        proxy = SocketProxy(ports=[2222])

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
                except (KeyboardInterrupt, asyncio.CancelledError):
                    break

            await proxy.stop()
            cluster.stop()

            cnt = 0
            while cnt < 3 and any(s.is_available for s in instances):
                print(instances)
                await asyncio.sleep(5)
                cnt += 1


def run_sd_service():
    try:
        asyncio.run(main(sys.argv[1]))
    except KeyboardInterrupt:
        print('Interruption')


if __name__ == "__main__":
    run_sd_service()
