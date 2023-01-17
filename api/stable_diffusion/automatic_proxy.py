import asyncio
from datetime import datetime, timedelta, timezone
import pathlib
import sys
from typing import Optional

from yapapi import Golem
from yapapi.contrib.service.http_proxy import HttpProxyService, LocalHttpProxy
from yapapi.payload import vm
from yapapi.services import ServiceState, Cluster

examples_dir = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(examples_dir))


# the timeout after we commission our service instances
# before we abort this script
STARTING_TIMEOUT = timedelta(minutes=4)

# additional expiration margin to allow providers to take our offer,
# as providers typically won't take offers that expire sooner than 5 minutes in the future
EXPIRATION_MARGIN = timedelta(minutes=5)

cluster: Optional[Cluster] = None


class AutomaticService(HttpProxyService):
    @staticmethod
    async def get_payload():
        return await vm.repo(
            image_hash='17de6c863581d53355f7cdeb8ec5f6d7eb43604494ea958a9dfe3ef7',
            image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-automatic-golem-latest-7c4666b6aa.gvmi',
            capabilities=['vpn', 'cuda*'],
        )

    async def start(self):
        async for script in super().start():
            yield script

        # start the remote HTTP server and give it some content to serve in the `index.html`
        script = self._ctx.new_script()
        script.run("run_service.sh")
        yield script

    # we don't need to implement `run` since, after the service is started,
    # all communication is performed through the VPN


async def main(port):
    global cluster

    async with Golem(
        budget=10.0,
        subnet_tag='public',
    ) as golem:
        commissioning_time = datetime.now()

        network = await golem.create_network("192.168.0.1/24")
        cluster = await golem.run_service(
            AutomaticService,
            instance_params=[{"remote_port": port}],
            network=network,
            num_instances=1,
            expiration=datetime.now(timezone.utc) + timedelta(days=365)
        )
        instances = cluster.instances

        def still_starting():
            return any(i.state in (ServiceState.pending, ServiceState.starting) for i in instances)

        # wait until all remote http instances are started

        while still_starting() and datetime.now() < commissioning_time + STARTING_TIMEOUT:
            print(f"instances: {instances}")
            await asyncio.sleep(5)

        if still_starting():
            raise Exception(
                f"Failed to start instances after {STARTING_TIMEOUT.total_seconds()} seconds"
            )

        # service instances started, start the local HTTP server

        proxy = LocalHttpProxy(cluster, port)
        await proxy.run()

        print(
            f"Local HTTP server listening on:\nhttp://localhost:{port}"
        )

        # wait until Ctrl-C

        start_time = datetime.now()

        while datetime.now() < start_time + timedelta(days=365):
            print(instances)
            try:
                await asyncio.sleep(10)
            except (KeyboardInterrupt, asyncio.CancelledError):
                break

        # perform the shutdown of the local http server and the service cluster

        await proxy.stop()
        print(f"HTTP server stopped")

        cluster.stop()

        await network.remove()


if __name__ == "__main__":
    try:
        asyncio.run(main(7861))
    except KeyboardInterrupt:
        print('Interruption')
    finally:
        print('Stopping cluster')
        cluster.stop()
