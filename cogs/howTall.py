import discord
from discord.ext import commands
from random import randint


class Howtall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howTall(self, ctx):
        ctx.send("Not enough")


def setup(bot):
    bot.add_cog(Howtall(bot))
