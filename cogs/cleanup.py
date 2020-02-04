import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime, timedelta
import asyncio
from config import bot


class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot.loop.create_task(self.attendance_tracker())

    async def daily(self, hour, minute):
        date = datetime.now(timezone('US/Eastern'))
        target = date.replace(hour=hour, minute=minute, second=0)
        if date >= target:
            target = target + timedelta(days=1)
        wait_for = int((target-date).total_seconds())
        await asyncio.sleep(wait_for)

    async def attendance_tracker(self):
        while True:
            await self.daily(12, 0)
            fng_list = await self.fng_finder()
            banned_nicknames = []
            banned_usernames = []
            warned_nicknames = []
            warned_usernames = []
            for fng in fng_list:
                diff, warned_date = await self.day_counter(fng)
                if diff.days > 30:
                    today_date = datetime.now(timezone('US/Eastern')).date()
                    if warned_date:
                        days_since_warned = today_date - warned_date
                        if days_since_warned.days > 15:
                            nickname, username = await self.ban_message(fng)
                            banned_nicknames.append(nickname)
                            banned_usernames.append(username)
                            continue
                    if not warned_date:
                        warned = datetime.now(timezone('US/Eastern'))
                        await self.bot.conn.execute("""
                        UPDATE date_joined SET warned_date = $1
                        WHERE date_joined.user_id = $2;
                        """, warned, fng)
                        nickname, username = await self.warning_message(fng)
                        warned_nicknames.append(nickname)
                        warned_usernames.append(username)
            await self.warned_admin_notification(warned_nicknames, warned_usernames)
            await self.banned_admin_notification(banned_nicknames, banned_usernames)

    async def day_counter(self, user_id):
        results = await self.bot.conn.fetchrow("""
        SELECT join_date, warned_date FROM date_joined WHERE user_id = $1;
        """, user_id)
        join_date, warned_date = results
        today_date = datetime.now(timezone('US/Eastern')).date()
        return today_date - join_date, warned_date

    async def fng_finder(self):
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        fng = discord.utils.get(guild.roles, name="fng")
        safe = discord.utils.get(guild.roles, name="safe")
        fng_list = []
        for member in guild.members:
            if fng in member.roles and \
                safe not in member.roles:
                fng_list.append(member.id)
        return fng_list

    async def warning_message(self, user_id):
        warning_msg = {
            'description' : "```WARNING: We've noticed you haven't attended a mission yet. New members are expected to attend their first mission within 30 days of joining, per the New Member Requirements agreed upon in the #rules channel.```",
            'thumbnail' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png',
            'field_1' : "If you have any scheduling issues preventing you from attending your first mission, please contact a **Moderator** or **Admin** letting us know when you plan on being able to attend. We understand life comes first, don't worry.",
            'field_2' : "If you neglect to contact a Staff member and fail to attend a mission within the next 15 days, you will be automatically banned. If you would like to play with us in the future, you will be required to submit another application on our website."
        }

        em = discord.Embed(description=warning_msg['description'], color=0xFFA500)
        em.set_author(name='The Cooler Server', icon_url=self.bot.user.avatar_url)
        em.set_thumbnail(url=warning_msg['thumbnail'])
        em.add_field(name="**SCHEDULING CONFLICTS**", value=warning_msg['field_1'], inline=False)
        em.add_field(name="**FAILURE TO ATTEND**", value=warning_msg['field_2'], inline=False)

        guild = self.bot.get_guild(self.bot.guilds[0].id)
        member = guild.get_member(user_id)
        await member.send(embed=em)
        nickname = member.display_name
        username = member.name+'#'+member.discriminator
        return nickname, username

    async def ban_message(self, user_id):
        ban_msg = {
            'description' : "```ATTENTION: You have been automatically banned from The Cooler Server due to failing to attend your first mission within the first 30 days.```If you would like to try playing with us again, please wait 24 hours and [submit another application](https://www.thecoolerserver.com/login/do/register).",
            'thumbnail' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png',
            'image' : 'https://i.redd.it/kfc2fd0kpnp21.jpg'
        }

        em = discord.Embed(description=ban_msg['description'], color=0xFF0000)
        em.set_thumbnail(url=ban_msg['thumbnail'])
        em.set_author(name='The Cooler Server', icon_url=self.bot.user.avatar_url)
        em.set_image(url=ban_msg['image'])

        guild = self.bot.get_guild(self.bot.guilds[0].id)
        member = guild.get_member(user_id)
        await member.send(embed=em)
        nickname = member.display_name
        username = member.name+'#'+member.discriminator
        await guild.ban(member, reason="Inactivity", delete_message_days=0)
        return nickname, username

    async def banned_admin_notification(self, nicknames, usernames):
        if not usernames:
            return
        channel = discord.utils.get(self.bot.get_all_channels(), name='server-management')
        desc = "```The following users have been BANNED for inactivity:```"
        em = discord.Embed(
            description=desc, color=0xFF0000)
        em.set_author(name='Attendance Enforcer', icon_url=self.bot.user.avatar_url)
        num = 0
        for nickname, username in zip(nicknames, usernames):
            num+=1
            em.add_field(name="{}. {}".format(str(num), nickname), value='*{}*'.format(username), inline=True)
        await channel.send(embed=em)

    async def warned_admin_notification(self, nicknames, usernames):
        if not usernames:
            return
        channel = discord.utils.get(self.bot.get_all_channels(), name='server-management')
        desc = "```The following users have been WARNED for inactivity:```"
        em = discord.Embed(
            description=desc, color=0xFFA500)
        em.set_author(name='Attendance Enforcer', icon_url=self.bot.user.avatar_url)
        num = 0
        for nickname, username in zip(nicknames, usernames):
            num+=1
            em.add_field(name="{}. {}".format(str(num), nickname), value='*{}*'.format(username), inline=True)
        await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Cleanup(bot))