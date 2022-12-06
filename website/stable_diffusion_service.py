import asyncio
from aioprocessing import AioQueue
from typing import Optional
import uuid

from yapapi import Golem
from yapapi.log import enable_default_logger
from yapapi.payload import vm
from yapapi.services import Service, ServiceState, Cluster

from pubsub import publish_job_status


enable_default_logger(log_file="sd-golem-service.log")

cluster: Optional[Cluster] = None
q: Optional[AioQueue] = None


class GenerateImageService(Service):
    def __init__(self, *args, instance_name: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = instance_name

    @staticmethod
    async def get_payload():
        return await vm.repo(
            # VM image placed at private server.
            image_hash='7b4c3af105db6b00b78b57752a0808919755c1f00ae6a78b9b85ffed',
            image_url='http://116.203.41.115:8000/docker-diffusers-golem-latest-3fdf198f2f.gvmi',
        )

    async def start(self):
        async for script in super().start():
            yield script
        script = self._ctx.new_script()
        script.run("run_service.sh")
        yield script

    async def run(self):
        while True:
            print(f'{self.name} RUN: waiting for next job')
            job = await q.coro_get()

            await publish_job_status(job["job_id"], "running")

            print(f'{self.name} RUN: running generation for: {job["prompt"]}')
            script = self._ctx.new_script()
            run_result = script.run('generate.sh', job["prompt"])
            yield script
            await run_result

            script = self._ctx.new_script()
            script.download_file('/usr/src/app/output/img.png', f'images/{job["job_id"]}.png')
            print(f'{self.name} RUN: finished job {job["job_id"]} ({job["prompt"]})')
            await publish_job_status(job["job_id"], "finished")
            yield script


async def main(num_instances):
    async with Golem(budget=10.0, subnet_tag="sd-test") as golem:
        global cluster
        cluster = await golem.run_service(
            GenerateImageService,
            instance_params=[{"instance_name": f"sd-service-{i + 1}"} for i in range(num_instances)],
        )

        def still_starting():
            return any(i.state in (ServiceState.pending, ServiceState.starting) for i in cluster.instances)

        while still_starting():
            print_instances()
            await asyncio.sleep(5)

        while True:
            await asyncio.sleep(60)
            print_instances()

            instance_to_reset = next((i for i in cluster.instances if i.state == ServiceState.terminated), None)
            if instance_to_reset is not None:
                print(f'{instance_to_reset.name} needs restart.')
                # TODO: find out how to reset an instance
                # await instance_to_reset.reset()


def print_instances():
    print(
        f"instances: "
        + str(
            [
                f"{s.name}: {s.state.value}"
                + (f" on {s.provider_name}" if s.provider_id else "")
                for s in cluster.instances
            ]
        )
    )


def run_sd_service(main_process_queue):
    global q
    q = main_process_queue
    try:
        asyncio.run(main(2))
    except KeyboardInterrupt:
        print('STOPPING CLUSTER')
        cluster.stop()


if __name__ == '__main__':
    q = AioQueue()
    q.put({'prompt': 'random hero', 'job_id': str(uuid.uuid4())})
    q.put({'prompt': 'astronaut on a horse', 'job_id': str(uuid.uuid4())})
    q.put({'prompt': 'cat on a bike', 'job_id': str(uuid.uuid4())})
    q.put({'prompt': 'dog on a surf board', 'job_id': str(uuid.uuid4())})
    run_sd_service(q)
