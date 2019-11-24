import discord
from pytz import timezone
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from pathlib import Path


class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            sleep_time = 60 - datetime.now(timezone('US/Eastern')).second
            await asyncio.sleep(sleep_time)
            await self.wait_until()

    async def get_next_mission(self, current):
        wednesday = timedelta((7 + 2 - current.weekday()) % 7)
        friday = timedelta((7 + 4 - current.weekday()) % 7)
        saturday = timedelta((7 + 5 - current.weekday()) % 7)
        op_days = [wednesday, friday, saturday]
        target = min(op_days)
        return (current + target).replace(hour=21, minute=0, second=0)

    async def wait_until(self):
        briefing_channel = discord.utils.get(self.bot.get_all_channels(), name='mission-briefing')
        while True:
            await asyncio.sleep(60)
            current = datetime.now(timezone('US/Eastern'))
            op = await self.get_next_mission(current)
            if op.weekday() == 2:
                op_name = "Wednesday"
            elif op.weekday() == 4:
                op_name = "Friday"
            elif op.weekday() == 5:
                op_name = "Saturday"
            countdown = op - current
            if countdown.total_seconds() <= 0:
                await briefing_channel.edit(topic="{} Op is going on now! Join the server!".format(op_name))
                await asyncio.sleep(10860) #Waits for 3 hours and 1 minute (12:01 the next day)
                break
            await self.countdown_updater(countdown, op_name, briefing_channel)

    async def countdown_updater(self, countdown, op_name, briefing_channel):
        days = str(countdown.days)
        plur_day = "days"
        if days == "1":
            plur_day = "day"
        hours = str(countdown.seconds // 3600)
        plur_hour = "hours"
        if hours == "1":
            plur_hour = "hour"
        minutes = str((countdown.seconds // 60) % 60)
        plur_minute = "minutes"
        if minutes == "1":
            plur_minute = "minute"
        await briefing_channel.edit(topic="Next Op [{}]: Starts in {} {} {} {} {} {}".format(
            op_name, days, plur_day, hours, plur_hour, minutes, plur_minute))


def setup(bot):
    bot.add_cog(Countdown(bot))
