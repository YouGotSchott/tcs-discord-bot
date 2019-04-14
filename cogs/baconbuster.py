import discord
from discord.ext import commands


class BaconBuster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = str(message.content)
        msg = msg.replace(" ", "")
        if message.author.id == 206380629523300352 \
                and msg.startswith('<:') \
                and msg.endswith('>'):
            await message.delete()


def setup(bot):
    bot.add_cog(BaconBuster(bot))
