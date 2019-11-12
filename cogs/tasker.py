import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime, timedelta
import asyncio
import psycopg2
from config import bot

class Tasker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        bot.loop.create_task(self.purge(guild))

    async def daily(self, hour, minute):
        date = datetime.now(timezone('US/Eastern'))
        target = date.replace(hour=hour, minute=minute, second=0)
        if date >= target:
            target = target + timedelta(days=1)
        wait_for = int((target-date).total_seconds())
        await asyncio.sleep(wait_for)

    async def purge(self, guild):
        while True:
            await self.daily(3, 0)
            channel = discord.utils.get(self.bot.get_all_channels(), name='server-management')
            members = await guild.prune_members(days=30, reason='Scheduled Purge')
            if members > 0:
                await channel.send("Pruned {} member(s) from the server.".format(str(members)))
            else:
                continue


def setup(bot):
    bot.add_cog(Tasker(bot))