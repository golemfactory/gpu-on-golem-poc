import asyncio
import copy
import cv2
from datetime import timedelta
from typing import AsyncIterable

from yapapi import Golem, Task, WorkContext
from yapapi.log import enable_default_logger
from yapapi.payload import vm


enable_default_logger(log_file="sd-golem.log")


async def _worker(context: WorkContext, tasks: AsyncIterable[Task]):
    dir_script = context.new_script()
    dir_script.run('/bin/mkdir', '-p', '/usr/src/app/output/input_frames')
    dir_script.run('/bin/mkdir', '-p', '/usr/src/app/output/output')
    yield dir_script

    async for task in tasks:
        # 3. Send JSON file and frames to provider
        script = context.new_script()
        params_data = copy.deepcopy(task.data)
        for i, path in enumerate(params_data['frames']):
            params_data['frames'][i] = f'output/input_frames/{path}'
        script.upload_json(params_data, '/usr/src/app/output/params.json')
        yield script

        upload_script = context.new_script()
        for frame in task.data['frames']:
            upload_script.upload_file(f'input_frames/{frame}', f'/usr/src/app/output/input_frames/{frame}')
        yield upload_script

        # 4. Run processing
        run_script = context.new_script()
        run_script.run("run_task.sh", "cuda", "output/params.json")
        yield run_script

        # 5. Download output frames
        download_script = context.new_script()
        future_result = None
        for frame in task.data['frames']:
            future_result = download_script.download_file(f'/usr/src/app/output/output/{frame}', f'output_frames/{frame}')
        yield download_script

        task.accept_result(result=await future_result)


async def _generate_on_golem():
    package = await vm.repo(
        image_hash="e40f1843a182418bd9f8ad5159eba37b8b14dd797f9f0fb62877bfdd",
        image_url='http://gpu-on-golem.s3.eu-central-1.amazonaws.com/docker-video-test-latest-c32f027bcb.gvmi',
        capabilities=['vpn', 'cuda*'],
    )

    # 1. Extract frames
    frames = []
    vid = cv2.VideoCapture("yoga.mp4")
    current_frame = 0
    while True:
        success, frame = vid.read()
        if frame is None:
            break
        frame_name = f'frame_{current_frame}.jpg'
        frame_path = f'input_frames/{frame_name}'
        cv2.imwrite(frame_path, frame)
        frames.append(frame_name)
        current_frame += 1

    # 2. Prepare JSON with params and list of frames and chunk it
    job_params = {
        'prompt': "((Anime art style)). An asian woman meditating in a room, light colours.",
        'negative_prompt': "blurry, blown-out, saturated, speckles, noise, dust, blotches, realistic, deformed face, dismembered, ugly, maximalistic",
        'image_strength': 0.63,
        'prompt_guidance': 20,
        'seed': 1026,
        'frames': [],
    }

    tasks = []
    chunk_size = 50
    frames_chunks = (frames[i:i + chunk_size] for i in range(0, len(frames), chunk_size))
    for chunk in frames_chunks:
        task_data = job_params.copy()
        task_data['frames'] = chunk
        tasks.append(Task(data=task_data))

    async with Golem(budget=10.0, subnet_tag="public") as golem:
        async for _ in golem.execute_tasks(_worker, tasks, payload=package, timeout=timedelta(minutes=180),
                                           max_workers=2):
            pass

    # TODO:
    #  6. Glue frames into movie. This process depends on the movie (framerate, resolution).


def generate_image():
    asyncio.run(_generate_on_golem())


if __name__ == "__main__":
    generate_image()
