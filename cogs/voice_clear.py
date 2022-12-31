import discord
from discord.ext import commands
import asyncio
import datetime as dt
import pytz


class VoiceClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        managed_channels = []
        managed_channels.append(discord.utils.get(self.bot.get_all_channels(), name="voice-text"))
        # managed_channels.append(discord.utils.get(self.bot.get_all_channels(), name="politics"))

        while True:
            sleep_time = await self.every_fifteen_minutes()
            await asyncio.sleep(sleep_time)

            for channel in managed_channels:
                msgs = await self.get_expired_messages(channel)
                if len(msgs) > 100:
                    await channel.delete_messages(msgs[-100:])
                else:
                    await channel.delete_messages(msgs)

    async def every_fifteen_minutes(self):
        while True:
            current = discord.utils.utcnow()
            output = current + (dt.datetime.min.replace(tzinfo=pytz.UTC) - current) % dt.timedelta(minutes=15)
            next_check = (output - current).seconds
            if next_check > 0:
                return next_check
            await asyncio.sleep(1)

    async def get_expired_messages(self, channel):
        msgs_all = [msg async for msg in channel.history(limit=5000)]
        return [
            x
            for x in msgs_all
            if (discord.utils.utcnow() - x.created_at).total_seconds() >= 300 #86400
        ]


async def setup(bot):
    await bot.add_cog(VoiceClear(bot))
