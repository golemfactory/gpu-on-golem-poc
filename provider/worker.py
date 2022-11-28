import sys

from diffusers import StableDiffusionPipeline


if __name__ == '__main__':
    device = sys.argv[1]
    prompt = sys.argv[2]

    print(f'Device: {device}')
    print(f'Phrase: {prompt}')

    pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
    pipe = pipe.to(device)

    image = pipe(prompt).images[0]
    image.save("./output/img.png")
