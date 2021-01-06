import discord
import os
from discord.ext import commands
import extensions

client = commands.Bot(command_prefix=".", description="Le fils à Poutine", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("On")

for file in os.listdir("extensions"):
    if file[-3:] == ".py":
        try:
            client.load_extension(f"extensions.{file[:-3]}")
        except:
            pass

client.run("NjkxNjY4NDMzNTE1MDUzMDc2.XnjUbQ.f_WMQ-Hmj8Ikhtsz53RpQ8iRiH0")
