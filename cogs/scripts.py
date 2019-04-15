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
        root = Path('bash/bot/')
        name = Path('deploy')
        subprocess.call([str(root / name)])
        ctx.message.add_reaction('👍')

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def arma(self, ctx):
        root = Path('bash/arma/')
        msg = ctx.message.content
        if ' start' in msg:
            name = Path('start')
        elif ' stop' in msg:
            name = Path('stop')
        elif ' restart' in msg:
            name = Path('restart')
        subprocess.call([str(root / name)])
        ctx.message.add_reaction('👍')

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def ww2(self, ctx):
        root = Path('bash/ww2/')
        msg = ctx.message.content
        if ' start' in msg:
            name = Path('start')
        elif ' stop' in msg:
            name = Path('stop')
        elif ' restart' in msg:
            name = Path('restart')
        subprocess.call([str(root / name)])
        ctx.message.add_reaction('👍')

def setup(bot):
    bot.add_cog(Deploy(bot))
