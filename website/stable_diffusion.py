from datetime import timedelta
import asyncio
from typing import AsyncIterable

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm


enable_default_logger(log_file="sd-golem.log")


async def _worker(context: WorkContext, tasks: AsyncIterable[Task]):
    script = context.new_script()
    async for task in tasks:
        script.run("run.sh", "cuda", task.data['phrase'])
        future_result = script.download_file('/usr/src/app/output/img.png', f'images/{task.data["id"]}.png')
        yield script
        task.accept_result(result=await future_result)


async def _generate_on_golem(phrase, job_id):
    package = await vm.repo(
        image_hash="5080b041087e342f258955abfa2042cf1a162697b589b00964b923be",
        image_url='https://lukasz-glen.com/docker-diffusers-golem-latest-16ef828013.gvmi',
    )

    tasks = [Task(data={'phrase': phrase, 'id': job_id})]

    async with Golem(budget=10.0, subnet_tag="sd-test") as golem:
        async for _ in golem.execute_tasks(_worker, tasks, payload=package, timeout=timedelta(minutes=90),
                                           max_workers=1):
            pass


def generate_image(phrase, job_id):
    asyncio.run(_generate_on_golem(phrase, job_id))
