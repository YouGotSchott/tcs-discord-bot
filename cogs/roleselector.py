import discord
from pathlib import Path
import json


messages_path = str(Path('cogs/data/messages.json'))

emojis = {
    'mission-maker' : 'feelscornman:485958281458876416',
    'heretic' : '\U0001f300',
    'liberation' : 'finger_gun:300089586460131328',
    'r6siege' : '\U0001f308',
    'ricefields' : 'rice_fields:483791993370181632',
    'minecraft' : '\U000026cf',
    'flight-sims' : '\U0001f525',
    'vr' : 'iron_uncle:548645154454765568'
}
msg_embed = {
    'title' : '**TCS Role Selector**',
    'description' : '''
    Use this tool to select optional Discord roles.
    **DO NOT ABUSE THE BOT**
    ''',
    'thumbnail' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
} 
mission_maker = {
    'name' : '<:{}> @mission-maker'.format(emojis['mission-maker']),
    'value' : '''
    Provides access to our mission making channels, which **MAY HAVE SPOILERS**.
    __**Requirements:**__
    **1.** You **MUST** attend a Saturday Op before taking this role.
    **2.** **ONLY** select this role if you plan on making missions for TCS.
    **3.** **DO NOT** use this role to provide feedback or suggestions in the mission making channel, use **#debriefing**.
    **4.** Understand that we make missions differently than other units.
    **5.** Understand that this is not an easy job and you might not get it right the first time.
    '''
}
heretic = {
    'name' : '{} @heretic'.format(emojis['heretic']),
    'value' : '''
    Provides access to the **#heresy** channel.
    *A place for Warhammer 40K discussion and shitposting.*
    '''
}
liberation = {
    'name' : '<:{}> @liberation'.format(emojis['liberation']),
    'value' : '''
    Allows other members to ping you to play *Arma 3 Liberation* on our server.
    '''
}
r6siege = {
    'name' : '{} @r6siege'.format(emojis['r6siege']),
    'value' : '''
    Allows other members to ping you to play *Rainbow Six Siege*.
    '''
}
ricefields = {
    'name' : '<:{}> @ricefields'.format(emojis['ricefields']),
    'value' : '''
    Allows other members to ping you to play *Rising Storm 2: Vietnam*.
    '''
}
minecraft = {
    'name' : '{} @minecraft'.format(emojis['minecraft']),
    'value' : '''
    Allows other members to ping you to play *Minecraft* on our server.
    '''
}
flight_sims = {
    'name' : '{} @flight-sims'.format(emojis['flight-sims']),
    'value' : '''
    Allows other members to ping you to play *DCS* or *IL2*.
    '''
}
vr = {
    'name' : '<:{}> @vr'.format(emojis['vr']),
    'value' : '''
    Allows other members to ping you to play any *Virtual Reality Games*.
    '''
}
footer = {
    'footer' : '''
    Add reaction to recieve role.
    Remove reaction to remove role.
    '''
}

class RoleSelector:
    def __init__(self, client):
        self.client = client
    
    async def on_ready(self):
        channel = discord.utils.get(self.client.get_all_channels(), name='roles')
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
        await self.client.add_reaction(msg, emoji=emojis['mission-maker'])
        await self.client.add_reaction(msg, emoji=emojis['heretic'])
        await self.client.add_reaction(msg, emoji=emojis['liberation'])
        await self.client.add_reaction(msg, emoji=emojis['r6siege'])
        await self.client.add_reaction(msg, emoji=emojis['ricefields'])
        await self.client.add_reaction(msg, emoji=emojis['minecraft'])
        await self.client.add_reaction(msg, emoji=emojis['flight-sims'])
        await self.client.add_reaction(msg, emoji=emojis['vr'])

    async def on_reaction_add(self, reaction, user):
        channel = discord.utils.get(self.client.get_all_channels(), name='roles')
        if user.id == self.client.user.id:
            return
        if 'roles' != str(channel):
            return
        if reaction.emoji == '<:{}>'.format(emojis['mission-maker']):
            role = discord.utils.get(user.server.roles, name="mission-maker")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['heretic']):
            role = discord.utils.get(user.server.roles, name="heretic")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['liberation']):
            role = discord.utils.get(user.server.roles, name="liberation")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['r6siege']):
            role = discord.utils.get(user.server.roles, name="r6siege")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['ricefields']):
            role = discord.utils.get(user.server.roles, name="ricefields")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['minecraft']):
            role = discord.utils.get(user.server.roles, name="minecraft")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['flight-sims']):
            role = discord.utils.get(user.server.roles, name="flight-sims")
            await self.client.add_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['vr']):
            role = discord.utils.get(user.server.roles, name="vr")
            await self.client.add_roles(user, role)
    
    async def on_reaction_remove(self, reaction, user):
        channel = discord.utils.get(self.client.get_all_channels(), name='roles')
        if 'roles' != str(channel):
            return
        if reaction.emoji == '<:{}>'.format(emojis['mission-maker']):
            role = discord.utils.get(user.server.roles, name="mission-maker")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['heretic']):
            role = discord.utils.get(user.server.roles, name="heretic")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['liberation']):
            role = discord.utils.get(user.server.roles, name="liberation")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['r6siege']):
            role = discord.utils.get(user.server.roles, name="r6siege")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['ricefields']):
            role = discord.utils.get(user.server.roles, name="ricefields")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['minecraft']):
            role = discord.utils.get(user.server.roles, name="minecraft")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '{}'.format(emojis['flight-sims']):
            role = discord.utils.get(user.server.roles, name="flight-sims")
            await self.client.remove_roles(user, role)
        elif reaction.emoji == '<:{}>'.format(emojis['vr']):
            role = discord.utils.get(user.server.roles, name="vr")
            await self.client.remove_roles(user, role)

    async def embeder(self, msg_embed):
        em = discord.Embed(
            title=msg_embed['title'], description=msg_embed['description'], color=0x008080)
        em.set_thumbnail(url=msg_embed['thumbnail'])
        em.add_field(name=mission_maker['name'], value=mission_maker['value'], inline=True)
        em.add_field(name=heretic['name'], value=heretic['value'], inline=True)
        em.add_field(name=liberation['name'], value=liberation['value'], inline=True)
        em.add_field(name=r6siege['name'], value=r6siege['value'], inline=True)
        em.add_field(name=ricefields['name'], value=ricefields['value'], inline=True)
        em.add_field(name=minecraft['name'], value=minecraft['value'], inline=True)
        em.add_field(name=flight_sims['name'], value=flight_sims['value'], inline=True)
        em.add_field(name=vr['name'], value=vr['value'], inline=True)
        em.set_footer(text=footer['footer'])
        return em


def setup(client):
    client.add_cog(RoleSelector(client))
