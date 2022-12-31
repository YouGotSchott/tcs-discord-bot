import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from config import bot
from cogs.briefing import Briefing


class Tasker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        async with bot:
            bot.loop.create_task(self.purge(guild))
            bot.loop.create_task(self.mission_alert_message(guild))
            bot.loop.create_task(self.delete_attending_role(guild))

    async def daily(self, hour, minute):
        date = datetime.now(timezone("US/Eastern"))
        target = date.replace(hour=hour, minute=minute, second=0)
        if date >= target:
            target = target + timedelta(days=1)
        await discord.utils.sleep_until(target)

    async def weekly(self, weekday, hour, minute):
        """Day of week is between 0 (Monday) and 6 (Sunday)"""
        date = datetime.now(timezone("US/Eastern"))
        target = date.replace(hour=hour, minute=minute, second=0)
        target_date = await self.get_next_weekday(target, weekday)
        if date >= target_date:
            target_date = target_date + timedelta(days=7)
        await discord.utils.sleep_until(target_date)

    async def get_next_weekday(self, startdate, weekday):
        diff = timedelta((7 + weekday - startdate.weekday()) % 7)
        return startdate + diff

    async def purge(self, guild):
        while True:
            await self.daily(3, 0)
            channel = discord.utils.get(
                self.bot.get_all_channels(), name="server-management"
            )
            members = await guild.prune_members(days=30, reason="Scheduled Purge")
            if members > 0:
                await channel.send(
                    "Pruned {} member(s) from the server.".format(str(members))
                )
            else:
                continue

    async def mission_alert_message(self, guild):
        while True:
            await self.weekly(5, 20, 50)
            em = discord.Embed(
                title="The mission starts in 10 minutes!",
                description="\n> Connect to the server and join your **Squad Channel** on **TeamSpeak**",
                color=0xFFCC00,
            )
            em.set_thumbnail(
                url="https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2020_logo.png"
            )
            em.set_author(
                name="Time to join the server!",
                icon_url="https://www.iconsdb.com/icons/preview/white/bell-3-xxl.png",
            )
            em.add_field(
                name="\u200b",
                value="[Link to Roster](https://docs.google.com/spreadsheets/d/1ObWkVSrXvUjron4Q9hK6Fy_sYWE1b-w135A7CPGfwBs/edit#gid=652948312) | [Link to Briefing]({})".format(
                    await Briefing(self.bot).url_grab()
                ),
            )
            channel = discord.utils.get(
                self.bot.get_all_channels(), name="bot-commands"
            )
            role = discord.utils.get(guild.roles, name="attending")
            await channel.send("<@&{}>".format(role.id), embed=em)

    async def delete_attending_role(self, guild):
        while True:
            await self.weekly(6, 0, 0)
            role = discord.utils.get(guild.roles, name="attending")
            await role.delete()


async def setup(bot):
    await bot.add_cog(Tasker(bot))
