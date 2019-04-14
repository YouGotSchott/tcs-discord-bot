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
        subprocess.call(['./discordbot.sh'])


def setup(bot):
    bot.add_cog(Deploy(bot))
