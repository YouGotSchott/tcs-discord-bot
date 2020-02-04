import discord
from discord.ext import commands
from pathlib import Path
from config import bot
from pytz import timezone
from datetime import datetime
from collections import OrderedDict
import json
import asyncio


class Butler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.agreement_path = str(Path('cogs/data/agreement.json'))

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

    @commands.Cog.listener()
    async def on_ready(self):
        agreement = await self.opener()
        channel = discord.utils.get(self.bot.get_all_channels(), name='rules')
        try:
            self.msg = await channel.fetch_message(agreement['agreement_msg']['id'])
            text = await self.embeder(self.data())
            await self.msg.edit(embed=text)
        except:
            await self.creator(channel)
        agreement['agreement_msg'] = {}
        agreement['agreement_msg']['id'] = self.msg.id
        await self.closer(agreement)

    async def opener(self):
        with open(self.agreement_path, 'r') as f:
            return json.load(f)

    async def closer(self, messages):
        with open(self.agreement_path, 'w') as f:
            json.dump(messages, f)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.member = member
        role_check = await self.eject_checker(self.member)
        if not role_check:
            return
        self.role = discord.utils.get(self.member.guild.roles, name='restricted')
        await self.member.add_roles(self.role)

    async def eject_checker(self, member):
        roles_path = str(Path('cogs/data/roles.json'))
        with open(roles_path, 'r') as f:
            roles = json.load(f)
        if not roles.get(str(member.id)):
            with open(roles_path, 'w') as f:
                json.dump(roles, f)
            return True
        else:
            with open(roles_path, 'w') as f:
                json.dump(roles, f)
            return False

    async def db_check(self, user_id):
        result = await self.bot.conn.fetchrow("""
        SELECT join_date FROM date_joined WHERE user_id = $1;
        """, user_id)
        if not result:
            await self.date_joined(user_id)
            return False
        else:
            return True

    async def date_joined(self, user_id):
        joined = datetime.now(timezone('US/Eastern'))
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        member = guild.get_member(int(user_id))
        nickname = member.display_name
        await self.bot.conn.execute("""
        INSERT INTO date_joined (user_id, nickname, join_date)
        VALUES ($1, $2, $3)
        """, user_id, nickname, joined)

    async def creator(self, channel):
            text = await self.embeder(self.data())
            self.msg = await channel.send(embed=text)
            await self.msg.add_reaction('\U00002705')
            await self.msg.add_reaction('\U0001f6ab')

    async def embeder(self, rules):
        em = discord.Embed(
            title=self.rules['title'], description=self.rules['description'], color=0x008080)
        em.set_thumbnail(url=self.rules['thumbnail'])
        for value in self.rule_list.values():
            em.add_field(name=value['name'], value=value['value'], inline=False)
        em.set_footer(text="Accept: \U00002705 | Decline: \U0001f6ab")
        return em

    async def join_message(self, member):
        channel = discord.utils.get(self.bot.get_all_channels(), name='general')
        greet = await channel.send('{} has joined the server!'.format(member.mention))
        await greet.add_reaction('\U0001f44b')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def agreement_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        channel = discord.utils.get(self.bot.get_all_channels(), name='rules')
        agreement = await self.opener()
        try:
            msg = await channel.fetch_message(agreement['agreement_msg']['id'])
        except KeyError:
            return
        try:
            if payload.message_id != msg.id:
                return
        except AttributeError:
            return
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(member.guild.roles, name='restricted')
        if role not in member.roles:
            await msg.remove_reaction(payload.emoji, member)
            return
        if str(payload.emoji) == '\U00002705':
            await self.accept(member, role)
        elif str(payload.emoji) == '\U0001f6ab':
            await self.decline(member)
        await msg.remove_reaction(payload.emoji, member)

    async def accept(self, member, role):
        await member.remove_roles(role)
        fng = discord.utils.get(member.guild.roles, name='fng')
        if await self.db_check(member.id):
            return
        await member.add_roles(fng)
        await self.join_message(member)

    async def decline(self, member):
        await member.kick(reason="Declined rule agreement")

    def data(self):
        self.rules = OrderedDict([
            ('title', '**__TCS RULE AGREEMENT__**'),
            ('description', '''
            ```Accepting this agreement is MANDATORY for entry into our Discord. By clicking ACCEPT, you acknowledge that you have read and understand the below rules.```
            '''),
            ('thumbnail', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
        )])
        self.rule_list = OrderedDict([
            ('title_1', OrderedDict([
                ('name', "**__CODE OF CONDUCT__**"),
                ('value', "_ _")])
            ),
            ('rule_1', OrderedDict([
                ('name', "**1.** Do not have fun at the expense of others"),
                ('value', "*We're a community, please treat others with respect*")])
            ),
            ('rule_2', OrderedDict([
                ('name', "**2.** Do not compromise the spirit of the mission"),
                ('value', """*Don't try to "break" missions to win*""")])
            ),
            ('rule_3', OrderedDict([
                ('name', "**3.** Do not use slurs or bigoted language"),
                ('value', """*...regardless of mission setting or context*
                \u200B""")])
            ),
            ('title_2', OrderedDict([
                ('name', "**__NEW MEMBER REQUIREMENTS__**"),
                ('value', "_ _")])
            ),
            ('rule_4', OrderedDict([
                ('name', "**1.** Your first mission must be on a Wednesday or Friday night"),
                ('value', "*These are smaller missions that will be easier to navigate on your first night*")])
            ),
            ('rule_5', OrderedDict([
                ('name', "**2.** You must show up one hour before your first mission"),
                ('value', """*Orientation is necessary, regardless of your familiarity with Arma 3*""")])
            ),
            ('rule_6', OrderedDict([
                ('name', "**3.** Attend your first mission 30 days after joining"),
                ('value', "*The Cooler Server is an Arma 3 unit, not just a Discord server*")])
            ),
        ])


def setup(bot):
    bot.add_cog(Butler(bot))