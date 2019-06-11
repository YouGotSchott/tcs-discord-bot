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

    @commands.group()
    async def whitelist(self, ctx, *args):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction('👎')

    @whitelist.command()
    async def add(self, ctx, *args):
        await self.poller('add', args[0])
        await ctx.message.add_reaction('👍')

    @whitelist.command()
    @commands.has_any_role('admin', 'moderator', 'helper')
    async def remove(self, ctx, *args):
        await self.poller('remove', args[0])
        await ctx.message.add_reaction('👍')

    async def poller(self, command, username):
        import asyncio
        cmd = ['bash/mc-wl', command, username]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while output is not None:
            retcode = output.poll()
            if retcode is not None:
                return
            else:
                await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(Deploy(bot))
