import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime
from config import bot
import asyncio

class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toggle = False

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def startsignup(self, ctx):
        self.bot.fake_toggle = False
        self.toggle = True
        self.uid_list = []
        await asyncio.sleep(5400)
        self.toggle = False
        self.uid_list.clear()

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def stopsignup(self, ctx):
        self.toggle = False
        self.uid_list.clear()

    @commands.command()
    async def role(self, ctx, *args):
        if self.bot.fake_toggle == True:
            await self.fake_signup(ctx)
        if self.toggle == False:
            return
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        fng = discord.utils.get(guild.roles, name="fng")
        if fng in ctx.message.author.roles:
            await ctx.message.add_reaction('👎')
            return
        uid = ctx.message.author.id
        if uid in self.uid_list:
            await ctx.message.add_reaction('👎')
            return
        roles = []
        for arg in args:
            roles.append(arg.replace(',','').strip(' '))
        if len(roles) == 0:
            roles = ['']
        roles = roles[slice(0, min(3, len(roles)))]
        self.date = datetime.now(timezone('US/Eastern'))
        user_data = {
            'user_id' : ctx.message.author.id,
            'nickname' : ctx.message.author.display_name,
            'date' : self.date,
            'roles' : roles,
        }
        await self.writer(user_data)
        self.uid_list.append(uid)
        await ctx.message.add_reaction('👍')

    async def writer(self, user_data):
        await self.bot.conn.execute("""
        INSERT INTO attendance (user_id, nickname, date)
        VALUES ($1, $2, $3)
        """, user_data['user_id'], user_data['nickname'], user_data['date'])
        for role in user_data['roles']:
            await self.bot.conn.execute("""
            INSERT INTO roles (attendance_id, role)
            VALUES ((SELECT id FROM attendance WHERE attendance.user_id = $1 
            AND attendance.date = $2), $3)
            """, user_data['user_id'], user_data['date'], role)

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def remove(self, ctx):
        if self.toggle == False:
            return
        user_id = ctx.message.mentions[0].id
        await self.bot.conn.execute("""
        DELETE FROM roles WHERE attendance_id = (SELECT id FROM attendance WHERE attendance.user_id = $1 
        AND attendance.date = $2)
        """, user_id, self.date)
        await self.bot.conn.execute("""
        DELETE FROM attendance WHERE user_id = $1
        AND date = $2""", user_id, self.date)
        self.uid_list.remove(user_id)
        await ctx.message.add_reaction('👍')

    async def fake_signup(self, ctx):
        user = ctx.author
        role = discord.utils.get(user.guild.roles, name='silenced')
        await user.add_roles(role)
        await asyncio.sleep(30)
        await user.remove_roles(role)

    @commands.command()
    async def joined(self, ctx):
        user_id = ctx.author.id
        result = await self.bot.conn.fetchrow("""
        SELECT join_date FROM date_joined WHERE user_id = $1;
        """, user_id)
        if not result:
            await ctx.message.add_reaction('👎')
            return
        joined_date = result[0].strftime("%d %B, %Y")
        await ctx.send(joined_date)


def setup(bot):
    bot.add_cog(Attendance(bot))