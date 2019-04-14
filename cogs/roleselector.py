import discord
from discord.ext import commands
from pathlib import Path
import json


messages_path = str(Path('cogs/data/messages.json'))

# emojis = {
#     'mission-maker' : '\U0001f52b',
#     'heretic' : '\U0001f300',
#     'liberation' : '\U0001f308',
#     'r6siege' : '\U0001f3c3',
#     'ricefields' : '\U0001f44d',
#     'minecraft' : '\U000026cf',
#     'flight-sims' : '\U0001f525',
#     'vr' : '\U000026a0',
#     'got' : '\U0001f409'
# }
emojis = {
    'mission-maker' : 'feelscornman:485958281458876416',
    'heretic' : '\U0001f300',
    'liberation' : 'finger_gun:300089586460131328',
    'r6siege' : '\U0001f308',
    'ricefields' : 'rice_fields:483791993370181632',
    'minecraft' : '\U000026cf',
    'flight-sims' : '\U0001f525',
    'vr' : 'iron_uncle:548645154454765568',
    'got' : '\U0001f409'
}
msg_embed = {
    'title' : '**TCS Role Selector**',
    'description' : '''
    Use this tool to select optional Discord roles.
    **DO NOT ABUSE THE BOT**
    *Reactions are removed on occasion, but this does not affect your roles.*
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
    Allows other members to ping you to play *Arma 3 Liberation* on our guild.
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
    Allows other members to ping you to play *Minecraft* on our guild.
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
got = {
    'name' : '{} @got'.format(emojis['got']),
    'value' : '''
    Provides access to the **#got-spoilers** channel.
    *A place for discussing Game of Thrones Season 8*
    '''
}
footer = {
    'footer' : '''
    Add reaction to recieve role.
    Remove reaction to remove role.
    '''
}

class RoleSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()    
    async def on_ready(self):
        channel = discord.utils.get(self.bot.get_all_channels(), name='roles')
        text = await self.embeder(msg_embed)
        with open(messages_path, 'r') as f:
            messages = json.load(f)
        try:
            msg = await channel.fetch_message(messages['role_message']['id'])
            await msg.delete()
            msg = await channel.send(embed=text)
        except:
            print("Role Message hasn't been added yet")
            msg = await channel.send(embed=text)
        messages['role_message'] = {}
        messages['role_message']['id'] = msg.id
        with open(messages_path, 'w') as f:
            json.dump(messages, f)
        await msg.add_reaction(emoji=emojis['mission-maker'])
        await msg.add_reaction(emoji=emojis['heretic'])
        await msg.add_reaction(emoji=emojis['liberation'])
        await msg.add_reaction(emoji=emojis['r6siege'])
        await msg.add_reaction(emoji=emojis['ricefields'])
        await msg.add_reaction(emoji=emojis['minecraft'])
        await msg.add_reaction(emoji=emojis['flight-sims'])
        await msg.add_reaction(emoji=emojis['vr'])
        await msg.add_reaction(emoji=emojis['got'])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        role_channel = discord.utils.get(self.bot.get_all_channels(), name='roles')
        if user.id == self.bot.user.id:
            return
        if str(reaction.message.channel.id) != str(role_channel.id):
            return
        if reaction.emoji == discord.utils.get(user.guild.emojis, name="feelscornman"):
            role = discord.utils.get(user.guild.roles, name="mission-maker")
            await user.add_roles(role)
        elif reaction.emoji == '{}'.format(emojis['heretic']):
            role = discord.utils.get(user.guild.roles , name="heretic")
            await user.add_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="finger_gun"):
            role = discord.utils.get(user.guild.roles, name="liberation")
            await user.add_roles(role)
        elif reaction.emoji == '{}'.format(emojis['r6siege']):
            role = discord.utils.get(user.guild.roles, name="r6siege")
            await user.add_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="rice_fields"):
            role = discord.utils.get(user.guild.roles, name="ricefields")
            await user.add_roles(role)
        elif reaction.emoji == '{}'.format(emojis['minecraft']):
            role = discord.utils.get(user.guild.roles, name="minecraft")
            await user.add_roles(role)
        elif reaction.emoji == '{}'.format(emojis['flight-sims']):
            role = discord.utils.get(user.guild.roles, name="flight-sims")
            await user.add_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="iron_uncle"):
            role = discord.utils.get(user.guild.roles, name="vr")
            await user.add_roles(role)
        elif reaction.emoji == '{}'.format(emojis['got']):
            role = discord.utils.get(user.guild.roles, name="got")
            await user.add_roles(role)
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        role_channel = discord.utils.get(self.bot.get_all_channels(), name='roles')
        if str(reaction.message.channel.id) != str(role_channel.id):
            return
        if reaction.emoji == discord.utils.get(user.guild.emojis, name="feelscornman"):
            role = discord.utils.get(user.guild.roles, name="mission-maker")
            await user.remove_roles(role)
        elif reaction.emoji == '{}'.format(emojis['heretic']):
            role = discord.utils.get(user.guild.roles, name="heretic")
            await user.remove_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="finger_gun"):
            role = discord.utils.get(user.guild.roles, name="liberation")
            await user.remove_roles(role)
        elif reaction.emoji == '{}'.format(emojis['r6siege']):
            role = discord.utils.get(user.guild.roles, name="r6siege")
            await user.remove_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="rice_fields"):
            role = discord.utils.get(user.guild.roles, name="ricefields")
            await user.remove_roles(role)
        elif reaction.emoji == '{}'.format(emojis['minecraft']):
            role = discord.utils.get(user.guild.roles, name="minecraft")
            await user.remove_roles(role)
        elif reaction.emoji == '{}'.format(emojis['flight-sims']):
            role = discord.utils.get(user.guild.roles, name="flight-sims")
            await user.remove_roles(role)
        elif reaction.emoji == discord.utils.get(user.guild.emojis, name="iron_uncle"):
            role = discord.utils.get(user.guild.roles, name="vr")
            await user.remove_roles(role)
        elif reaction.emoji == '{}'.format(emojis['got']):
            role = discord.utils.get(user.guild.roles, name="got")
            await user.remove_roles(role)

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
        em.add_field(name=got['name'], value=got['value'], inline=True)
        em.set_footer(text=footer['footer'])
        return em


def setup(bot):
    bot.add_cog(RoleSelector(bot))
