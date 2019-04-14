import discord
from discord.ext import commands
import subprocess


class Deploy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('admin')
    async def deploy(self, ctx):
        await ctx.message.delete()
        await subprocess.call(['ServiceRestart.bat'], shell=True)


def setup(bot):
    bot.add_cog(Deploy(bot))
