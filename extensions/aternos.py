import discord
from discord.ext import commands, tasks
from aternosapi import AternosAPI
from config import *
from sys import platform

server = AternosAPI(HEADER_TOKEN, TOKEN_AT)


class aternos(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update_status_message.start()

    @commands.command(name="server_start", brief="Start the aternos server")
    async def server_start(self, ctx):
        if server.GetStatus() == "Offline":
            server.StartServer()
            await ctx.send("The server is starting...")
        else:
            await ctx.send("The server is already online!")

    @commands.command(name="server_stop", brief="Stop the aternos server")
    async def server_stop(self, ctx):
        if ctx.guild.get_role(MCMANAGER) in ctx.author.roles:
            if server.GetStatus() == "Starting ..." or server.GetStatus() == "Online":
                server.StopServer()
                await ctx.send("The server is stopping..")
            else:
                await ctx.send("The server is already off")
        else:
            await ctx.send("You are not allowed to use this command")

    @commands.command(name="server_status", brief="Get the server status")
    async def server_status(self, ctx):
        await ctx.send(f"The server is {server.GetStatus().lower()}")

    @tasks.loop(seconds=10)
    async def update_status_message(self):
        await self.client.wait_until_ready()
        try:
            e = discord.Embed(
                title="Server status",
                description=server.GetStatus(),
                color=0x008000
            )
            await self.status_message.edit(embed=e, color=0x008000)
        except:
            channel = self.client.get_channel(CHANNEL_STATUS)
            e = discord.Embed(
                title="Server status",
                description=server.GetStatus(),
                color=0x008000
            )
            self.status_message = await channel.send(embed=e)


def setup(client):
    client.add_cog(aternos(client))
