import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from time import strftime


class BaconBuster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        msg = str(message.content)
        msg = msg.strip()
        if message.mentions:
            log_time = datetime.now(timezone('US/Eastern')).strftime("%m/%d/%Y %H:%M:%S")
            channel = discord.utils.get(self.bot.get_all_channels(), name='logging')
            await channel.send((f'{log_time} - **{message.author.mention}** deleted a user mention in {message.channel.mention} | '
                    f'**Message Content:** "{msg}"'))


def setup(bot):
    bot.add_cog(BaconBuster(bot))