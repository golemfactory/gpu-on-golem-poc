import json
import sys
import torch

from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image


if __name__ == '__main__':
    device = sys.argv[1]
    json_file = sys.argv[2]

    print(f'Device: {device}')
    print(f'Reading params from file: {json_file}')
    with open(json_file, 'r') as f:
        data = json.loads(f.read())

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained("./stable-diffusion-v1-5")
    pipe = pipe.to(device)

    step = 1
    for frame in data['frames']:
        original_image = Image.open(frame)

        torch.manual_seed(data['seed'])
        img = pipe(
            prompt=data['prompt'],
            init_image=original_image,
            negative_prompt=data['negative_prompt'],
            strength=data['image_strength'],
            guidance_scale=data['prompt_guidance'],
        )

        img.images[0].save(frame.replace('input_frames', 'output'))
