import discord
from discord.ext import commands
import subprocess
from pathlib import Path


class Deploy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('admin')
    async def deploy(self, ctx):
        root = Path('bash/')
        name = Path('deploy')
        await ctx.message.delete()
        subprocess.call([str(root / name)])

def setup(bot):
    bot.add_cog(Deploy(bot))
