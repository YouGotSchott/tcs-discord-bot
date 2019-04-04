import discord
from pathlib import Path
import json

messages_path = str(Path('cogs/data/messages.json'))

msg_embed = {
    'title' : '@mission-maker',
    'description' : '''
    
    This role gives access to the mission making channels. Everyone is free to give mission making a try.
    **__Requirements__**
    *> Attend at least 1 Saturday Op*
    *> Understand that we make missions differently than other units*
    ''',
    'name' : 'Mission Making',
}

class RoleSelector:
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        channel = self.client.get_channel('557248486324699176')
        with open(messages_path, 'r') as f:
            messages = json.load(f)
        try:
            msg = await self.client.get_message(channel, messages['role_message']['id'])
            await self.client.delete_message(msg)
        except KeyError:
            print("Role Message hasn't been added yet")
        text = await self.embeder(msg_embed)
        msg = await self.client.send_message(channel, embed=text)
        messages['role_message'] = {}
        messages['role_message']['id'] = msg.id
        with open(messages_path, 'w') as f:
            json.dump(messages, f)
        await self.client.add_reaction(msg, emoji='👍')

    async def on_reaction_add(self, reaction, user):
        channel = self.client.get_channel('557248486324699176')
        if user.id == self.client.user.id:
            return
        if 'roles' != str(channel):
            return
        if reaction.emoji == "👍":
            role = discord.utils.get(user.server.roles, name="test")
            await self.client.add_roles(user, role)
    
    async def on_reaction_remove(self, reaction, user):
        channel = self.client.get_channel('557248486324699176')
        if 'roles' != str(channel):
            return
        if reaction.emoji == "👍":
            role = discord.utils.get(user.server.roles, name="test")
            await self.client.remove_roles(user, role)

    async def embeder(self, msg_embed):
        em = discord.Embed(
            title=msg_embed['title'], description=msg_embed['description'], colour=0xDEADBF)
        em.set_author(name=msg_embed['name'],
                      icon_url=self.client.user.avatar_url)
        return em


def setup(client):
    client.add_cog(RoleSelector(client))
