import discord
from discord.ext import commands
from pathlib import Path
from config import bot
from collections import OrderedDict
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
        emojis = self.emoji_selector(self.bot.guilds[0].id)
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

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def role_reaction_add(self, payload):
        try:
            if payload.message_id != self.msg.id:
                return
        except AttributeError:
            return
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if user.id == self.bot.user.id:
            return
        emojis = self.emoji_selector(guild.id)
        clean_emoji = str(payload.emoji).strip('<:>')
        for k, v in emojis.items():
            if v in clean_emoji:
                role = discord.utils.get(user.guild.roles, name=k)
                if 'mission-maker' in k:
                    results = await self.saturday_check()
                    if user.id not in results:
                        await self.msg.remove_reaction(v, user)
                        return
                if 'auditor' in k:
                    role_mm = discord.utils.get(user.guild.roles, name='mission-maker')
                    if role_mm not in user.roles:
                        await self.msg.remove_reaction(v, user)
                        return
                if role in user.roles:
                    await user.remove_roles(role)
                else:
                    await user.add_roles(role)
                await self.msg.remove_reaction(v, user)

    async def saturday_check(self):
        results = await self.bot.conn.fetch("""
        SELECT user_id FROM attendance""")
        id_list = [x["user_id"] for x in results]
        return id_list

    async def embeder(self, msg_embed):
        em = discord.Embed(
            title=self.msg_embed['title'], description=self.msg_embed['description'], color=0x008080)
        em.set_thumbnail(url=self.msg_embed['thumbnail'])
        for value in self.field_dict.values():
            em.add_field(name=value['name'], value=value['value'], inline=False)
        em.set_footer(text=self.footer['footer'])
        return em

    def emoji_selector(self, guild):
        if 169696752461414401 == guild:
            emojis = OrderedDict([
                ('mission-maker', 'feelscornman:485958281458876416'),
                ('auditor', '\U0001F913'),
                ('heretic', '\U0001f300'),
                ('liberation', 'finger_gun:300089586460131328'),
                ('r6siege', '\U0001f308'),
                ('ricefields', 'rice_fields:483791993370181632'),
                ('minecraft', '\U000026cf'),
                ('flight-sims', '\U0001f525'),
                ('vr', 'iron_uncle:548645154454765568'),
                ('zeus-op', '\U000026a1'),
                ('4x', '\U0001f3ed'),
                ('rts', 'smoothbrain:592115163390410783'),
                ('destiny-2', '\U0001f47e'),
                ('squad', 'CplChad:409868955239579649'),
                ('zomboid', 'the_devil:663562931681624081'),
                ('tabletop', '\U0001f9d9\U0000200d\U00002642\U0000fe0f'),
                ('insurgency', 'jamsheed:713592883332251648')
            ])
        else:
            emojis = OrderedDict([
                ('mission-maker', 'uncle:567728566540697635'),
                ('auditor', '\U0001F913'),
                ('heretic', '\U0001f300'),
                ('liberation', 'snek_uncle:567728565781528576'),
                ('r6siege', '\U0001f3c3'),
                ('ricefields', 'shadow_uncle:567728565248851989'),
                ('minecraft', '\U000026cf'),
                ('flight-sims', '\U0001f525'),
                ('vr', 'jensen_uncle:567728565391589399'),
                ('zeus-op', '\U000026a1'),
                ('4x', '\U0001f3ed'),
                ('rts', 'fast_uncle:567728565525807104'),
                ('destiny-2', '\U0001f47e'),
                ('squad', 'uncle_uncle:567728565785985025'),
                ('zomboid', 'uncle_hacker:567728565798567940'),
                ('tabletop', '\U0001f9d9\U0000200d\U00002642\U0000fe0f'),
                ('insurgency', 'evil_uncle:567728565148450844')
            ])
        return emojis

    def data(self, emojis):
        self.msg_embed = OrderedDict([
            ('title', '**TCS Role Selector**'),
            ('description', '''Use this tool to select optional Discord roles.\n\n'''
            '''**DO NOT ABUSE THE BOT!**\n'''
            '''\u200B'''),
            ('thumbnail', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2020_logo.png')
        ])
        self.field_dict = OrderedDict([
            ('mission_maker', OrderedDict([
                ('name', '<:{}> @mission-maker'.format(emojis['mission-maker'])),
                ('value', '''Provides access to our mission making channels, which *MAY HAVE SPOILERS*.\n\n'''
                '''__**REQUIREMENTS**__\n'''
                '''**__1.)__** You **MUST** attend a Saturday Op before taking this role.\n'''
                '''**__2.)__** **ONLY** select this role if you plan on making missions for TCS.\n'''
                '''**__3.)__** **DO NOT** use this role to provide feedback or suggestions in the mission making channel, use **#debriefing**.\n'''
                '''**__4.)__** Understand that we make missions differently than other units.\n'''
                '''**__5.)__** Understand that this is not an easy job and you might not get it right the first time.\n'''
                '''\u200B''')])
            ),
            ('auditor', OrderedDict([
                ('name', '{} @auditor'.format(emojis['auditor'])),
                ('value', '''Allows other mission makers to ping you to check their missions for errors. *(requires @mission-maker tag)*\n''')])
            ),
            ('heretic', OrderedDict([
                ('name', '{} @heretic'.format(emojis['heretic'])),
                ('value', '''Provides access to the **#heresy** channel.\n'''
                '''*A place for Warhammer 40K discussion and shitposting.*''')])
            ),
            ('liberation', OrderedDict([
                ('name', '<:{}> @liberation'.format(emojis['liberation'])),
                ('value', '''Allows other members to ping you to play *Arma 3 Liberation* on our server.''')])
            ),
            ('r6siege', OrderedDict([
                ('name', '{} @r6siege'.format(emojis['r6siege'])),
                ('value', '''Allows other members to ping you to play *Rainbow Six Siege*.''')])
            ),
            ('ricefields', OrderedDict([
                ('name', '<:{}> @ricefields'.format(emojis['ricefields'])),
                ('value', '''Allows other members to ping you to play *Rising Storm 2: Vietnam*.''')])
            ),
            ('minecraft', OrderedDict([
                ('name', '{} @minecraft'.format(emojis['minecraft'])),
                ('value', '''Allows other members to ping you to play *Minecraft* on our server.''')])
            ),
            ('flight_sims', OrderedDict([
                ('name', '{} @flight-sims'.format(emojis['flight-sims'])),
                ('value', '''Allows other members to ping you to play *DCS* or *IL2*.''')])
            ),
            ('vr', OrderedDict([
                ('name', '<:{}> @vr'.format(emojis['vr'])),
                ('value', '''Allows other members to ping you to play any *Virtual Reality Games*.''')])
            ),
            ('zeus-op', OrderedDict([
                ('name', '{} @zeus-op'.format(emojis['zeus-op'])),
                ('value', '''Allows other members to ping you to play *Impromptu Zeus Missions*.\n\n'''
                '''__**RULES**__\n'''
                '''**__1.)__** Don't expect someone to step-up as Zeus.\n'''
                '''**__2.)__** Zeus has final say on what's allowed in their mission.\n'''
                '''\u200B''')])
            ),
            ('4x', OrderedDict([
                ('name', '{} @4x'.format(emojis['4x'])),
                ('value', '''Allows other members to ping you to play *4X Games*.\n\n'''
                '''__**Active Games**__\n'''
                '''> *Hearts of Iron 4*\n'''
                '''> *Stellaris*\n'''
                '''\u200B''')])
            ),
            ('rts', OrderedDict([
                ('name', '<:{}> @rts'.format(emojis['rts'])),
                ('value', '''Allows other members to ping you to play *RTS Games*.\n\n'''
                '''__**Active Games**__\n'''
                '''> *Wargame: Red Dragon*\n'''
                '''> *Wargame: War in the East*\n'''
                '''> *Men of War: Assault Squad 2*\n'''
                '''> *StarCraft 2*\n'''
                '''\u200B''')])
            ),
            ('destiny-2', OrderedDict([
                ('name', '{} @destiny-2'.format(emojis['destiny-2'])),
                ('value', '''Allows other members to ping you to play *Destiny 2*.\n\n'''
            )])
            ),
            ('squad', OrderedDict([
                ('name', '<:{}> @squad'.format(emojis['squad'])),
                ('value', '''Allows other members to ping you to play *Squad*.\n\n'''
            )])
            ),
            ('zomboid', OrderedDict([
                ('name', '<:{}> @zomboid'.format(emojis['zomboid'])),
                ('value', '''Allows other members to ping you to play organized *Project Zomboid*.\n\n'''
            )])
            ),
            ('tabletop', OrderedDict([
                ('name', '{} @tabletop'.format(emojis['tabletop'])),
                ('value', '''Gain access to the **Tabletop** channels to play organized tabletop games and DnD sessions.\n\n'''
            )])
            ),
            ('insurgency', OrderedDict([
                ('name', '<:{}> @insurgency'.format(emojis['insurgency'])),
                ('value', '''Allows other members to ping you to play organized [*Insurgency: Sandstorm*](https://store.steampowered.com/app/581320/Insurgency_Sandstorm/).\n\n'''
            )])
            )
        ])
        self.footer = OrderedDict([
            ('footer', '''React to toggle role on/off''')
        ])

def setup(bot):
    bot.add_cog(RoleSelector(bot))
