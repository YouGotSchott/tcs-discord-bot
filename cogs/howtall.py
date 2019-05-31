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
        await ctx.send("Not enough.")

    @commands.command()
    async def joined(self, ctx):
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        member = guild.get_member(ctx.message.author.id)
        arrival = member.joined_at
        arrival = arrival.strftime("%d %B, %Y")
        await ctx.send(arrival)


def setup(bot):
    bot.add_cog(HowTall(bot))
