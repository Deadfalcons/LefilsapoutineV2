from discord.ext import commands


class tests(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.by = "</Deadfalcon>"

    @commands.command(name="ping", brief="Pong!")
    async def ping(self, ctx):
        await ctx.send("Pong! :ping_pong:")


def setup(client):
    client.add_cog(tests(client))
