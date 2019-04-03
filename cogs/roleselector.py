import discord
from pathlib import Path
import json

# role_msg = str(Path('data/role_msg.json'))

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
        text = await self.embeder(msg_embed)
        msg = await self.client.send_message(channel, embed=text)
        # msg_id = {'id' : msg}
        await self.client.add_reaction(msg, emoji='👍')

    async def on_reaction_add(self, reaction, user):
        channel = self.client.get_channel('557248486324699176')
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
