import discord
from discord.ext import commands
from datetime import datetime
# from pytz import timezone
from time import strftime


class PingAbuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        msg = str(message.content)
        msg = msg.strip()
        if message.mentions:
            time_elapsed = discord.utils.utcnow() - message.created_at
            if time_elapsed.total_seconds() <= 3600:
                log_time = discord.utils.utcnow().replace(microsecond=0).timestamp()
                channel = discord.utils.get(self.bot.get_all_channels(), name='logging')
                await channel.send((f'<t:{int(log_time)}:f> - **{message.author.mention}** deleted a user mention in {message.channel.mention} | '
                        f'**Message Content:** "{msg}"'))


async def setup(bot):
    await bot.add_cog(PingAbuse(bot))