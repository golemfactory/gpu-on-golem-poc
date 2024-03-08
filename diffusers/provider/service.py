import asyncio
import json
import logging
import sys

from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from safetensors.torch import load_file
import portalocker
import torch


logging.basicConfig(filename='output/debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

STABLE_DIFFUSION_ITERATIONS_NUMBER = 5


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

unet = UNet2DConditionModel.from_config("./stable-diffusion-xl-base-1.0", subfolder="unet").to("cuda", torch.float16)
unet.load_state_dict(load_file("./sdxl_lightning_4step_unet.safetensors"))
pipe = StableDiffusionXLPipeline.from_pretrained("./stable-diffusion-xl-base-1.0", unet=unet, torch_dtype=torch.float16, variant="fp16").to(
    "cuda")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
pipe.enable_sequential_cpu_offload()


def latents_callback(i, t, latents):
    progress = int(i / (STABLE_DIFFUSION_ITERATIONS_NUMBER - 1) * 100)
    # Do not save 100% progress in callback. We want to do this when all is over.
    progress = progress if progress < 100 else None

    intermediary_img_path = None
    update_status(progress=progress, new_image_path=intermediary_img_path)


def update_status(progress: int = None, new_image_path: str = None):
    try:
        status_file = open('output/status.json', 'r')
    except FileNotFoundError:
        progress_info = {'progress': 0, 'images': []}
    else:
        progress_info = json.loads(status_file.read())
        status_file.close()

    if progress is not None:
        progress_info['progress'] = progress

    if new_image_path is not None:
        if 'images' not in progress_info:
            progress_info['images'] = []
        progress_info['images'].append(new_image_path)

    with portalocker.Lock('output/status.lock', timeout=2):
        with open('output/status.json', 'w') as f:
            f.write(json.dumps(progress_info))


async def main():
    while True:
        await asyncio.sleep(1)
        try:
            with open('phrase.txt', 'r+') as f:
                phrase = f.readline()
                if len(phrase.strip()) > 0:
                    logger.info('Running generation')
                    image = pipe(
                        phrase,
                        callback=latents_callback,
                        callback_steps=1,
                        num_inference_steps=4,
                        guidance_scale=0
                    ).images[0]
                    logger.info('Saving image')
                    rgb_img = image.convert('RGB')
                    rgb_img.save("./output/img.jpg", optimize=True, quality=80)
                    logger.info('Output file saved. Clearing phrase.txt file.')
                    f.truncate(0)
                    update_status(progress=100)
        except FileNotFoundError:
            open('phrase.txt', 'w').close()


if __name__ == '__main__':
    asyncio.run(main())
