import discord
from discord.ext import commands


class Swatter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await message.add_reaction('\U0001f5de')


def setup(bot):
    bot.add_cog(Swatter(bot))
