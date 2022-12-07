import sys
import logging
import asyncio

from diffusers import StableDiffusionPipeline


logging.basicConfig(filename='output/debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
pipe = pipe.to("cuda")


async def main():
    while True:
        logger.info('Sleeping for 2 sec...')
        await asyncio.sleep(2)
        logger.info('Checking file phrase.txt')
        try:
            with open('phrase.txt', 'r+') as f:
                phrase = f.readline()
                if len(phrase.strip()) > 0:
                    logger.info('Running generation')
                    image = pipe(phrase).images[0]
                    logger.info('Saving image')
                    image.save("./output/img.png")
                    logger.info('Output file saved. Clearing phrase.txt file.')
                    f.truncate(0)
                else:
                    logger.info('No phrase in file. Ignoring.')
        except FileNotFoundError:
            open('phrase.txt', 'w').close()


if __name__ == '__main__':
    asyncio.run(main())
