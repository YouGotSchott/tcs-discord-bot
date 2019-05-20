import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime
from config import db_user, db_pass, db_port
import asyncio
import psycopg2

class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.toggle = False
        self.aconn = psycopg2.connect(
            database='discord_bot', 
            user=db_user, 
            password=db_pass, 
            host='127.0.0.1', 
            port=db_port,
            async_=1)
        self.wait(self.aconn)
    
    def wait(self, conn):
        import select
        while True:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [])
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [])
            else:
                raise psycopg2.OperationalError("poll() returned %s" % state)

    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def startsignup(self, ctx):
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
        if self.toggle == False:
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
        d = datetime.now(timezone('US/Eastern'))
        self.date = d.strftime('%Y-%m-%d')
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
        acurs = self.aconn.cursor()
        acurs.execute("""
        INSERT INTO attendance (user_id, nickname, date)
        VALUES (%s, %s, %s)""", (user_data['user_id'], user_data['nickname'], user_data['date']))
        self.wait(acurs.connection)
        for role in user_data['roles']:
            acurs.execute("""
            INSERT INTO roles (attendance_id, role)
            VALUES ((SELECT id FROM attendance WHERE attendance.user_id = %s 
            AND attendance.date = %s), %s)""", (user_data['user_id'], user_data['date'], role))
            self.wait(acurs.connection)
    
    @commands.command()
    @commands.has_any_role('admin', 'moderator')
    async def remove(self, ctx):
        if self.toggle == False:
            return
        user_id = ctx.message.mentions[0].id
        acurs = self.aconn.cursor()
        acurs.execute("""
        DELETE FROM roles WHERE attendance_id = (SELECT id FROM attendance WHERE attendance.user_id = %s 
        AND attendance.date = %s)""", (user_id, self.date))
        self.wait(acurs.connection)
        acurs.execute("""
        DELETE FROM attendance WHERE user_id = %s
        AND date = %s""", (user_id, self.date))
        self.wait(acurs.connection)
        self.uid_list.remove(user_id)
        await ctx.message.add_reaction('👍')


def setup(bot):
    bot.add_cog(Attendance(bot))