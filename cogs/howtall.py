import discord
from discord.ext import commands


class HowTall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howtall(self, ctx):
        await ctx.send("https://tenor.com/view/beating-horse-south-dead-park-gif-3899971")

    @commands.command()
    async def dunkaccino(self, ctx):
        await ctx.send("https://tenor.com/view/beating-horse-south-dead-park-gif-3899971")

def setup(bot):
    bot.add_cog(HowTall(bot))
