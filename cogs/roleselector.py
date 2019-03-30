import discord
from discord.ext import commands

msgs = []

titles = [
    '@mission-maker',
    '@minecraft',
    '@eco'
]
descriptions = [
    '''
    This role gives access to the mission making channels. Everyone is free to give mission making a try.
    **__Requirements__**
    *> Attend at least 1 Saturday Op*
    *> Understand that we make missions differently than other units*
    ''',
    '''
    Allows other people who play Minecraft to ping your role directly.
    ''',
    '''
    Allows other people who play Eco to ping you about how there isn't a server anymore.
    '''
]
names = [
    'Mission Making',
    'Minecraft',
    'Eco'
]


class RoleSelector:
    def __init__(self, client):
        self.client = client

    async def on_reaction_add(self, reaction, ctx):
        roleChannelId = '557248486324699176'
        if reaction.message.channel.id != roleChannelId:
            return
        if reaction.emoji == "👍":
            user_id = ctx.reaction.server.get_member(ctx.message.author.id)
            await self.client.add_roles(user_id, '558351518831607831')

    @commands.command(pass_context=True)
    @commands.has_any_role('admin')
    async def embed(self, ctx):
        await self.client.delete_message(ctx.message)
        await self.rotation(ctx, msgs)

    async def post(self, ctx, msg_data):
        em = discord.Embed(
            title=msg_data['title'], description=msg_data['description'], colour=0xDEADBF)
        em.set_author(name=msg_data['name'],
                      icon_url=self.client.user.avatar_url)
        msg = await self.client.send_message(self.client.get_channel('557248486324699176'), embed=em)
        await self.client.add_reaction(msg, '👍')
        return msg

    async def dict_creator(self, title, description, name):
        msg_data = {
            'title': title,
            'description': description,
            'name': name
        }
        return msg_data

    async def remove(self, msgs):
        if msgs:
            await self.client.delete_messages(msgs)

    async def rotation(self, ctx, msgs):
        await self.remove(msgs)
        embed_msgs = zip(titles, descriptions, names)
        for title, description, name in embed_msgs:
            msg_data = await self.dict_creator(title, description, name)
            msg = await self.post(ctx, msg_data)
            msgs.append(msg)


def setup(client):
    client.add_cog(RoleSelector(client))
