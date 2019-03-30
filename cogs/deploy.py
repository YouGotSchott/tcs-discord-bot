import discord
from discord.ext import commands
import subprocess


class Deploy:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_role('admin')
    async def deploy(self, ctx):
        await self.client.delete_message(ctx.message)
        await subprocess.call(['ServiceRestart.bat'], shell=True)


def setup(client):
    client.add_cog(Deploy(client))
