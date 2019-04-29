import discord
from discord.ext import commands


class HowTall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howtall(self, ctx):
        await ctx.send("Not enough.")


def setup(bot):
    bot.add_cog(HowTall(bot))
