import asyncio
import json

import discord
from discord.ext import commands
import aiohttp
import io


intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True

with open("env.json","r") as fh:
    env = json.load(fh)

PREFIX = '/'

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
TOKEN = env["token"]

url = "https://gpu.dev-test.golem.network"

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    
async def get_job_detail(session, job_detail_url):
    async with session.get(job_detail_url) as status_response:
        status_response_json = await status_response.json()
        return status_response_json

@bot.command(name="generate", help="generate an image using Stable Diffusion")
async def generate(ctx):
    _, *args = ctx.message.content.split(" ")
    prompt = ' '.join(args)
    print('[INFO]',prompt)
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}/txt2img", data={"prompt": prompt}) as response:
            response_json = await response.json()
            job_detail_url = response_json["job_detail_url"]
            job_detail = await get_job_detail(session, job_detail_url)
            await ctx.reply(f"adding request: \"{prompt}\" to the queue (position {job_detail['queue_position']})")
            finished = False
            while not finished:
                job_detail = await get_job_detail(session, job_detail_url)
                finished = job_detail["status"] == 'finished'
                await asyncio.sleep(1)
                
        img_url = f"{url}/images/{job_detail['job_id']}.jpg"
        async with session.get(img_url) as response:
            img = await response.read()
            with io.BytesIO(img) as file:
                await ctx.reply(prompt, file=discord.File(file, f"{'_'.join(prompt.split())}.jpg"))


bot.run(TOKEN)

