import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from time import strftime


class BaconBuster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = str(message.content)
        msg = msg.strip()
        if msg.startswith('<@') and msg.endswith('>'):
            guild = self.bot.get_guild(self.bot.guilds[0].id)
            for user in message.mentions:
                log_time = datetime.now(timezone('US/Eastern')).strftime("%m/%d/%Y %H:%M:%S")
                member = guild.get_member(user.id)
                print(f"{log_time} - {message.author.display_name} has mentioned {member.display_name} without context")


def setup(bot):
    bot.add_cog(BaconBuster(bot))