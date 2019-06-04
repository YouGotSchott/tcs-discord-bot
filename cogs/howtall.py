import discord
from discord.ext import commands


class HowTall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howtall(self, ctx):
        still = [92362557439893504]
        if ctx.message.author.id in still:
            await ctx.send("__STILL__ not enough.")
            return
        await ctx.send("Not enough.")


def setup(bot):
    bot.add_cog(HowTall(bot))
