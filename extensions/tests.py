from discord.ext import commands
from datetime import datetime
import time

class tests(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.by = "</Deadfalcon>"

    @commands.Cog.listener()
    async def on_message(self, ctx):
        print(f"{ctx.author} {datetime.fromtimestamp(time.time()).strftime('%d/%m/%y %H:%M')} | {ctx.content}")

    @commands.command(name="ping", brief="Pong!")
    async def ping(self, ctx):
        await ctx.send("Pong! :ping_pong:")


def setup(client):
    client.add_cog(tests(client))
