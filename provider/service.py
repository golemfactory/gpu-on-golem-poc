import asyncio
import json
import logging
import sys

from diffusers import StableDiffusionPipeline
from PIL import Image
import torch


logging.basicConfig(filename='output/debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

STABLE_DIFFUSION_ITERATIONS_NUMBER = 51
UPDATE_PROGRESS_EVERY_STEPS_NUMBER = 3
intermediary_images_number: int = 0


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
pipe = pipe.to("cuda")
vae = pipe.vae


def latents_to_pil(latents):
    latents = (1 / 0.18215) * latents
    with torch.no_grad():
        image = vae.decode(latents).sample
    image = (image / 2 + 0.5).clamp(0, 1)
    image = image.detach().cpu().permute(0, 2, 3, 1).numpy()
    images = (image * 255).round().astype("uint8")
    pil_images = [Image.fromarray(image) for image in images]
    return pil_images


def latents_callback(i, t, latents):
    progress = int(i / (STABLE_DIFFUSION_ITERATIONS_NUMBER - 1) * 100)
    # Do not save 100% progress in callback. We want to do this when all is over.
    progress = progress if progress < 100 else None

    intermediary_img_path = None
    if intermediary_images_number > 0:
        iterations_to_generate = set(
            list(
                range(0, STABLE_DIFFUSION_ITERATIONS_NUMBER - 1,
                      int((STABLE_DIFFUSION_ITERATIONS_NUMBER - 1) / intermediary_images_number)
                      )
            )[:intermediary_images_number]
        )
        if i in iterations_to_generate:
            image = latents_to_pil(latents)
            rgb_img = image[0].convert('RGB').resize((256, 256))
            intermediary_img_path = f"output/iteration_{i}.jpg"
            rgb_img.save(intermediary_img_path, optimize=True, quality=50)

    if i % UPDATE_PROGRESS_EVERY_STEPS_NUMBER == 0:
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
                    image = pipe(phrase, callback=latents_callback, callback_steps=1).images[0]
                    logger.info('Saving image')
                    image.save("./output/img.png")
                    logger.info('Output file saved. Clearing phrase.txt file.')
                    f.truncate(0)
                    update_status(progress=100)
        except FileNotFoundError:
            open('phrase.txt', 'w').close()


if __name__ == '__main__':
    intermediary_images_number = int(sys.argv[1])
    asyncio.run(main())
