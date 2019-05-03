import discord
from discord.ext import commands
from random import randint
from pathlib import Path
import json


class Eject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_path = str(Path('cogs/data/roles.json'))

    @commands.command()
    async def eject(self, ctx):
        username = ctx.message.author.display_name
        luck = randint(1, 5)
        if luck == 1:
            await ctx.send("*{} hit the canopy on the way out!*".format(username))
            await self.role_grabber(ctx.message.author)
            await self.invite_maker(ctx.message)
            await ctx.message.author.kick()
        else:
            await ctx.send("*has kicked {} from the server!*".format(username))

    async def opener(self):
        with open(self.roles_path, 'r') as f:
            return json.load(f)

    async def closer(self, roles):
        with open(self.roles_path, 'w') as f:
            json.dump(roles, f)

    async def role_grabber(self, user):
        role_list = []
        for role in user.roles:
            role_list.append(role.name)
        roles = await self.opener()
        roles[str(user.id)] = {}
        roles[str(user.id)]['roles'] = role_list
        await self.closer(roles)

    async def invite_maker(self, message):
        invite = await message.channel.create_invite(max_age=24, max_uses=1)
        dm = await message.author.create_dm()
        await dm.send(invite)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.role_giver(member)

    async def role_giver(self, member):
        roles = await self.opener()
        if not roles.get(str(member.id)):
            await self.closer(roles)
            return
        for role in roles[str(member.id)]['roles']:
            if role == '@everyone':
                continue
            role_add = discord.utils.get(member.guild.roles, name=role)
            await member.add_roles(role_add)
        del roles[str(member.id)]
        await self.closer(roles)


def setup(bot):
    bot.add_cog(Eject(bot))
