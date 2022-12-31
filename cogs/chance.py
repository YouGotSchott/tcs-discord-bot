import discord
from discord.ext import commands
import aiohttp
import random
import asyncio


class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx):
        toss = random.randint(0, 1)
        async with ctx.channel.typing():
            await asyncio.sleep(2)
            if toss == 0:
                await ctx.send("Heads")
            else:
                await ctx.send("Tails")

    @commands.command()
    async def d20(self, ctx):
        roll = random.randint(1, 20)
        async with ctx.channel.typing():
            indef = "a"
            if roll in [8, 11, 18]:
                indef = "an"
            await asyncio.sleep(1)
            await ctx.send(f"{ctx.message.author.display_name} rolled {indef} {roll}")


async def setup(bot):
    await bot.add_cog(Chance(bot))
