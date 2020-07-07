import discord
from pytz import timezone
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio


class Cooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            time_current = datetime.now(timezone('US/Eastern'))
            time_mission = await self.get_next_mission(time_current)
            sleep_time = (time_mission - time_current).total_seconds()
            await asyncio.sleep(sleep_time)
            await self.set_lockdown(time_mission)

    @commands.command()
    @commands.has_any_role('admin')
    async def unlock(self, ctx):
        await self.remove_lock(ctx.channel)

    async def get_next_mission(self, current):
        wednesday = timedelta((7 + 2 - current.weekday()) % 7)
        friday = timedelta((7 + 4 - current.weekday()) % 7)
        saturday = timedelta((7 + 5 - current.weekday()) % 7)
        op_days = [wednesday, friday, saturday]
        target = min(op_days)
        return (current + target).replace(hour=21, minute=0, second=0)

    async def set_lockdown(self, day):
        channel = await self.find_channel(day)

        em = discord.Embed(
            title="Debrief Cooldown - ON",
            description="`Channel will open for discussion in 9 Hours (6 AM Eastern Time)`",
            color=0xFF0000
        )

        lock_message = await channel.send(embed=em)
        await channel.set_permissions(channel.guild.default_role, send_messages=False, add_reactions=False)
        await asyncio.sleep(32400) # Waits 9 hours before unlocking channel
        await lock_message.delete()
        await self.remove_lock(channel)

    async def find_channel(self, day):
        if day.weekday() == 2:
            channel = discord.utils.get(self.bot.get_all_channels(), name='wed-mission-debriefing')
        elif day.weekday() == 4:
            channel = discord.utils.get(self.bot.get_all_channels(), name='fri-mission-debriefing')
        elif day.weekday() == 5:
            channel = discord.utils.get(self.bot.get_all_channels(), name='sat-mission-debriefing')
        return channel

    async def remove_lock(self, channel):
        await channel.set_permissions(channel.guild.default_role, send_messages=None, add_reactions=None)

        em = discord.Embed(
            title="Debrief Cooldown - OFF",
            description="`Channel is now open to discuss last night's mission`",
            color=0x008000
        )

        await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Cooldown(bot))
