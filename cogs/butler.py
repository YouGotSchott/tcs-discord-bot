import discord
from discord.ext import commands
from pathlib import Path
import json
import asyncio


class Butler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.agreement_path = str(Path('cogs/data/agreement.json'))

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
        agreement = await self.opener()
        dm = await self.member.create_dm()
        try:
            self.msg = await dm.fetch_message(agreement[str(self.member.id)]['id'])
        except:
            await self.creator(dm, self.member)
        agreement[str(self.member.id)] = {}
        agreement[str(self.member.id)]['id'] = self.msg.id
        await self.closer(agreement)
        try:
            self.bot.loop.create_task(await self.timeout())
        except:
            return

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

    async def timeout(self):
        await asyncio.sleep(30)
        try:
            await self.msg.delete()
            await self.member.kick(reason="Failed to accept rule agreement in alotted time")
        except:
            return

    async def creator(self, dm, member):
            text = await self.embeder(self.data())
            self.msg = await dm.send(embed=text)
            await self.member.add_roles(self.role)
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
        await channel.send('{} has joined the server!'.format(member.mention))

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def agreement_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        user = self.bot.get_user(payload.user_id)
        agreement = await self.opener()
        try:
            msg = await user.fetch_message(agreement[str(user.id)]['id'])
        except KeyError:
            return
        try:
            if payload.message_id != msg.id:
                return
        except AttributeError:
            return
        guild = self.bot.get_guild(544217233560436779)
        member = guild.get_member(payload.user_id)
        if str(payload.emoji) == '\U00002705':
            await self.accept(msg, member, agreement)
        elif str(payload.emoji) == '\U0001f6ab':
            await self.decline(msg, member, agreement)

    async def accept(self, msg, member, agreement):
        role = discord.utils.get(member.guild.roles, name='restricted')
        await member.remove_roles(role)
        await self.join_message(member)
        await msg.remove_reaction('\U0001f6ab', self.bot.user)
        del agreement[str(member.id)]
        self.msg = None
        await self.closer(agreement)

    async def decline(self, msg, member, agreement):
        await msg.delete()
        del agreement[str(member.id)]
        await self.closer(agreement)
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