import discord
from discord.ext import commands
import asyncio
import datetime as dt


class VoiceClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        voice_text = discord.utils.get(self.bot.get_all_channels(), name="voice-text")

        while True:
            sleep_time = await self.every_fifteen_minutes()
            await asyncio.sleep(sleep_time)
            msgs = await self.get_expired_messages(voice_text)
            if len(msgs) > 100:
                await voice_text.delete_messages(msgs[-100:])
            else:
                await voice_text.delete_messages(msgs)

    async def every_fifteen_minutes(self):
        while True:
            current = dt.datetime.now()
            output = current + (dt.datetime.min - current) % dt.timedelta(minutes=15)
            next_check = (output - current).seconds
            if next_check > 0:
                return next_check
            await asyncio.sleep(1)

    async def get_expired_messages(self, channel):
        msgs_all = await channel.history(limit=5000).flatten()
        return [
            x
            for x in msgs_all
            if (dt.datetime.now() - x.created_at).total_seconds() >= 86400
        ]


def setup(bot):
    bot.add_cog(VoiceClear(bot))
