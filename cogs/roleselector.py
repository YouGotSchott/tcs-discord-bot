import discord
from discord.ext import commands
from pathlib import Path
import json


class RoleSelector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages_path = str(Path('cogs/data/messages.json'))

    async def opener(self):
        with open(self.messages_path, 'r') as f:
            return json.load(f)

    async def closer(self, messages):
        with open(self.messages_path, 'w') as f:
            json.dump(messages, f)

    @commands.Cog.listener()    
    async def on_ready(self):
        emojis = self.emoji_selector(self.bot.guilds)
        channel = discord.utils.get(self.bot.get_all_channels(), name='roles')
        text = await self.embeder(self.data(emojis))
        messages = await self.opener()
        try:
            self.msg = await channel.fetch_message(messages['role_message']['id'])
            await self.msg.edit(embed=text)
        except:
            print("Role Message hasn't been added yet")
            self.msg = await channel.send(embed=text)
        messages['role_message'] = {}
        messages['role_message']['id'] = self.msg.id
        await self.closer(messages)
        for emoji in emojis.values():
            await self.msg.add_reaction(emoji=emoji)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        emojis = self.emoji_selector(guild)
        user = guild.get_member(payload.user_id)
        clean_emoji = str(payload.emoji).strip('<:>')
        if user.id == self.bot.user.id:
            return
        if payload.message_id != self.msg.id:
            return
        for k, v in emojis.items():
            if v in clean_emoji:
                role = discord.utils.get(user.guild.roles, name=k)
                await user.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        emojis = self.emoji_selector(guild)
        user = guild.get_member(payload.user_id)
        clean_emoji = str(payload.emoji).strip('<:>')
        if user.id == self.bot.user.id:
            return
        if payload.message_id != self.msg.id:
            return
        for k, v in emojis.items():
            if v in clean_emoji:
                role = discord.utils.get(user.guild.roles, name=k)
                await user.remove_roles(role)

    async def embeder(self, msg_embed):
        em = discord.Embed(
            title=self.msg_embed['title'], description=self.msg_embed['description'], color=0x008080)
        em.set_thumbnail(url=self.msg_embed['thumbnail'])
        for value in self.field_dict.values():
            em.add_field(name=value['name'], value=value['value'], inline=True)
        em.set_footer(text=self.footer['footer'])
        return em
    
    def emoji_selector(self, guild):
        guild_list = []
        guild_list.append(guild)
        if 169696752461414401 in guild_list:
            emojis = {
                'mission-maker' : 'feelscornman:485958281458876416',
                'heretic' : '\U0001f300',
                'liberation' : 'finger_gun:300089586460131328',
                'r6siege' : '\U0001f308',
                'ricefields' : 'rice_fields:483791993370181632',
                'minecraft' : '\U000026cf',
                'flight-sims' : '\U0001f525',
                'vr' : 'iron_uncle:548645154454765568',
                'got' : '\U0001f409',
                'zeus-op' : '\U000026a1'
            }
        else:
            emojis = {
                'mission-maker' : 'uncle:567728566540697635',
                'heretic' : '\U0001f300',
                'liberation' : 'snek_uncle:567728565781528576',
                'r6siege' : '\U0001f3c3',
                'ricefields' : 'shadow_uncle:567728565248851989',
                'minecraft' : '\U000026cf',
                'flight-sims' : '\U0001f525',
                'vr' : 'jensen_uncle:567728565391589399',
                'got' : '\U0001f409',
                'zeus-op' : '\U000026a1'
            }
        return emojis

    def data(self, emojis):
        self.msg_embed = {
            'title' : '**TCS Role Selector**',
            'description' : '''
            Use this tool to select optional Discord roles.
            **DO NOT ABUSE THE BOT**
            *Reactions are removed on occasion, but this does not affect your roles.*
            ''',
            'thumbnail' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
        }
        self.field_dict = {
            'mission_maker' : {
                'name' : '<:{}> @mission-maker'.format(emojis['mission-maker']),
                'value' : '''
                Provides access to our mission making channels, which **MAY HAVE SPOILERS**.
                __**REQUIREMENTS:**__
                **1.** You **MUST** attend a Saturday Op before taking this role.
                **2.** **ONLY** select this role if you plan on making missions for TCS.
                **3.** **DO NOT** use this role to provide feedback or suggestions in the mission making channel, use **#debriefing**.
                **4.** Understand that we make missions differently than other units.
                **5.** Understand that this is not an easy job and you might not get it right the first time.
                '''
            },
            'heretic' : {
                'name' : '{} @heretic'.format(emojis['heretic']),
                'value' : '''
                Provides access to the **#heresy** channel.
                *A place for Warhammer 40K discussion and shitposting.*
                '''
            },
            'liberation' : {
                'name' : '<:{}> @liberation'.format(emojis['liberation']),
                'value' : '''
                Allows other members to ping you to play *Arma 3 Liberation* on our guild.
                '''
            },
            'r6siege' : {
                'name' : '{} @r6siege'.format(emojis['r6siege']),
                'value' : '''
                Allows other members to ping you to play *Rainbow Six Siege*.
                '''
            },
            'ricefields' : {
                'name' : '<:{}> @ricefields'.format(emojis['ricefields']),
                'value' : '''
                Allows other members to ping you to play *Rising Storm 2: Vietnam*.
                '''
            },
            'minecraft' : {
                'name' : '{} @minecraft'.format(emojis['minecraft']),
                'value' : '''
                Allows other members to ping you to play *Minecraft* on our guild.
                '''
            },
            'flight_sims' : {
                'name' : '{} @flight-sims'.format(emojis['flight-sims']),
                'value' : '''
                Allows other members to ping you to play *DCS* or *IL2*.
                '''
            },
            'vr' : {
                'name' : '<:{}> @vr'.format(emojis['vr']),
                'value' : '''
                Allows other members to ping you to play any *Virtual Reality Games*.
                '''
            },
            'got' : {
                'name' : '{} @got'.format(emojis['got']),
                'value' : '''
                Provides access to the **#got-spoilers** channel.
                *A place for discussing Game of Thrones Season 8*
                '''
            },
            'zeus-op' : {
                'name' : '{} @zeus-op'.format(emojis['zeus-op']),
                'value' : '''
                Allows other memebers to ping you to play *Impromptu Zeus Missions*.
                __**RULES:**__
                **1.** Don't expect someone to step-up as Zeus.
                **2.** Zeus has final say on what's allowed in their mission.
                '''
            }
        }
        self.footer = {
            'footer' : '''
            Add reaction to recieve role.
            Remove reaction to remove role.
            '''
        }

def setup(bot):
    bot.add_cog(RoleSelector(bot))
