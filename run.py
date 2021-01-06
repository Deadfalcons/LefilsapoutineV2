import datetime

import discord
import os
from discord.ext import commands
import time
from datetime import datetime

client = commands.Bot(command_prefix=".", description="Le fils a Poutine", intents=discord.Intents.all())
# test comment

@client.event
async def on_ready():
    print("On")

@client.event
async def on_message(ctx):
    print(f"{ctx.author} {datetime.fromtimestamp(time.time()).strftime('%d/%m/%y %H:%M')} | {ctx.content}")

for file in os.listdir("extensions"):
    if file[-3:] == ".py":
        try:
            client.load_extension(f"extensions.{file[:-3]}")
        except:
            pass

client.run("NjkxNjY4NDMzNTE1MDUzMDc2.XnjUbQ.f_WMQ-Hmj8Ikhtsz53RpQ8iRiH0")
