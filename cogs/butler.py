import discord
from discord.ext import commands
from pathlib import Path
import json
import asyncio


class Butler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.agreement_path = str(Path('cogs/data/agreement.json'))

    @commands.Cog.listener()
    async def on_ready(self):
        agreement = await self.opener()
        channel = discord.utils.get(self.bot.get_all_channels(), name='rules')
        try:
            self.msg = await channel.fetch_message(agreement['agreement_msg']['id'])
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
            em.add_field(name=value['name'], value=value['value'], inline=True)
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
        guild = self.bot.get_guild(544217233560436779)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(member.guild.roles, name='restricted')
        if role not in member.roles:
            return
        if str(payload.emoji) == '\U00002705':
            await self.accept(member, role)
        elif str(payload.emoji) == '\U0001f6ab':
            await self.decline(member)

    async def accept(self, member, role):
        await member.remove_roles(role)
        fng = discord.utils.get(member.guild.roles, name='fng')
        await member.add_roles(fng)
        await self.join_message(member)

    async def decline(self, member):
        await member.kick(reason="Declined rule agreement")

    def data(self):
        self.rules = {
            'title' : 'TCS Rule Agreement',
            'description' : '''
            This is a placeholder rule agreement for The Cooler Server
            Continue to the Discord Server by reacting on '\U00002705'.
            ''',
            'thumbnail' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
        }
        self.rule_list = {
            'rule_1' : {
                'name' : 'Rule One Name',
                'value' : 'Description of Rule One'
            },
            'rule_2' : {
                'name' : 'Rule Two Name',
                'value' : 'Description of Rule Two'
            }
        }


def setup(bot):
    bot.add_cog(Butler(bot))