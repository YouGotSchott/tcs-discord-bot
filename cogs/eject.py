import discord
from discord.ext import commands
from random import randint


class Eject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eject(self, ctx):
        username = ctx.message.author.display_name
        luck = randint(1, 20)
        if luck == 20:
            await ctx.send("*{} hit the canopy on the way out!*".format(username))
            user_id = self.bot.get_user(ctx.message.author)
            await user_id.kick()
        else:
            await ctx.send("*has kicked {} from the server!*".format(username))


def setup(bot):
    bot.add_cog(Eject(bot))
