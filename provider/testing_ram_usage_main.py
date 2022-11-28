import sys
import datetime

from diffusers import StableDiffusionPipeline


if __name__ == '__main__':
    input1 = input("Please press 'Enter' to continue.")
    device = sys.argv[1]
    prompt = sys.argv[2]

    print(f'Device: {device}')
    print(f'Phrase: {prompt}')
    

    pipe = StableDiffusionPipeline.from_pretrained("./stable-diffusion-v1-5")
    pipe = pipe.to(device)

    image = pipe(prompt).images[0]
    image.save("./output/img.png")
    
    new_prompt = input("Please, provide new prompt for the model and press enter to continue: ")

    image = pipe(new_prompt).images[0]
    image.save("./output/img.png")
    
    input("Please press 'Enter' to continue.")