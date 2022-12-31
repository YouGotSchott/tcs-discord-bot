import discord
from pytz import timezone
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio


class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.brief_wed = discord.utils.get(self.bot.get_all_channels(), name='wed-mission-briefing')
        self.brief_fri = discord.utils.get(self.bot.get_all_channels(), name='fri-mission-briefing')
        self.brief_sat = discord.utils.get(self.bot.get_all_channels(), name='sat-mission-briefing')

        while True:
            sleep_time = await self.every_five_minutes(datetime.now())
            await asyncio.sleep(sleep_time)
            op_days = [2, 4, 5]
            for op_day in op_days:
                await asyncio.sleep(1)
                await self.wait_for(op_day)

    async def every_five_minutes(self, current):
        while True:
            output = current + (datetime.min - current) % timedelta(minutes=10)
            return (output - current).seconds

    async def get_next_mission(self, op_day, current):
        op = timedelta((7 + op_day - current.weekday()) % 7)
        return (current + op).replace(hour=21, minute=0, second=0)

    async def wait_for(self, op_day):
        if op_day == 2:
            op_name = "Wednesday"
            briefing_channel = self.brief_wed
        elif op_day == 4:
            op_name = "Friday"
            briefing_channel = self.brief_fri
        elif op_day == 5:
            op_name = "Saturday"
            briefing_channel = self.brief_sat

        current = datetime.now(timezone('US/Eastern'))
        op = await self.get_next_mission(op_day, current)
        current = current - timedelta(minutes=current.minute % 5,
                             seconds=current.second,
                             microseconds=current.microsecond)
        countdown = op - current

        if (current.weekday() == op_day) and (current >= current.replace(hour=21, minute=0, second=0)):
            await briefing_channel.edit(topic="{} Op is going on now! Join the server!".format(op_name))
        else:
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
        await briefing_channel.edit(topic="{} Op Starts in ~{} {} {} {} {} {}".format(
            op_name, days, plur_day, hours, plur_hour, minutes, plur_minute))


async def setup(bot):
    await bot.add_cog(Countdown(bot))
