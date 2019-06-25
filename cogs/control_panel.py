import discord
from discord.ext import commands
from pathlib import Path
from collections import OrderedDict
import json


class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.panel = str(Path('cogs/data/panel.json'))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.msg_setup()

    async def opener(self):
        with open(self.panel, 'r') as f:
            return json.load(f)

    async def closer(self, panel):
        with open(self.panel, 'w') as f:
            json.dump(panel, f)

    async def msg_setup(self):
        panel = await self.opener()
        channel = discord.utils.get(self.bot.get_all_channels(), name='control-panel')
        self.emojis = OrderedDict([
            ('\U000025b6', 'start'),
            ('\U000023f9', 'stop'),
            ('\U0001f501', 'restart'),
            ('\U00002705', 'hc_start'),
            ('\U0000274e', 'hc_stop'),
            ('\U00002733', 'hc_restart')
        ])
        server = OrderedDict([
            ('instructions', OrderedDict([
                ('title', 'INSTRUCTIONS'),
                ('url', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'),
                ('color', 0x008080)])
            ),
            ('arma', OrderedDict([
                ('title', 'ARMA 3 SERVER'),
                ('url', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/main_sil.png'),
                ('color', 0xFF0000)])
            ),
            ('ww2', OrderedDict([
                ('title', 'ARMA 3 WW2 SERVER'),
                ('url', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/ww2_sil.png'),
                ('color', 0xFF5733)])
            ),
            ('minecraft', OrderedDict([
                ('title', 'MINECRAFT'),
                ('url', 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'),
                ('color', 0xF4D03F)])
            )
        ])
        panel = await self.opener()
        if not panel.values():
            for key, value in server.items():
                print("Control panel message hasn't been created yet.")
                if value['title'] == 'INSTRUCTIONS':
                    text = await self.intro_embeder(value['title'], value['url'], value['color'])
                    msg = await channel.send(embed=text)
                    panel[key] = msg.id
                    continue
                if value['title'] == 'MINECRAFT':
                    text = await self.embeder(value['title'], value['url'], value['color'])
                    msg = await channel.send(embed=text)
                    panel[key] = msg.id
                    for index, moji in zip(range(3), self.emojis.keys()):
                        if index == 3:
                            continue
                        await msg.add_reaction(emoji=moji)
                else:
                    text = await self.embeder(value['title'], value['url'], value['color'])
                    msg = await channel.send(embed=text)
                    panel[key] = msg.id
                    for moji in self.emojis.keys():
                        await msg.add_reaction(emoji=moji)
        else:
            for p_value, p_key, s_value in zip(panel.values(), panel.keys(), server.values()):
                msg = await channel.fetch_message(p_value)
                if s_value['title'] == 'INSTRUCTIONS':
                    text = await self.intro_embeder(s_value['title'], s_value['url'], s_value['color'])
                else:
                    text = await self.embeder(s_value['title'], s_value['url'], s_value['color'])
                panel[p_key] = msg.id
                await msg.edit(embed=text)
        await self.closer(panel)
        self.panel_dict = await self.opener()

    async def intro_embeder(self, server_title, server_url, color):
        desc = '''
        ```Use the following reactions to perform actions on the server. Your reaction will be removed once the action has completed.```
        \U000025b6 Start the Server
        \U000023f9 Stop the Server
        \U0001f501 Restart the Server
        \U00002705 Start the Headless Client
        \U0000274e Stop the Headless Client
        \U00002733 Restart the Headless Client
        '''
        foot = 'The bot will show as "typing" while the action is runnning.'
        em = discord.Embed(
            title=server_title, description=desc, color=color)
        em.set_thumbnail(url=server_url)
        em.set_footer(text=foot)
        return em

    async def embeder(self, server_title, server_url, color):
        desc = '_ _'
        foot = 'The bot will show as "typing" while the action is runnning.'
        em = discord.Embed(
            title=server_title, description=desc, color=color)
        em.set_thumbnail(url=server_url)
        em.set_footer(text=foot)
        return em

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def control_reaction(self, payload):
        try:
            if payload.message_id not in self.panel_dict.values():
                return
        except AttributeError:
            return
        if payload.user_id == self.bot.user.id:
            return
        for key, value in self.emojis.items():
            if key in str(payload.emoji):
                channel = discord.utils.get(self.bot.get_all_channels(),
                    name='control-panel')
                async with channel.typing():
                    await self.scripts(self.panel_dict, 
                        payload.message_id, value)
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    message = await channel.fetch_message(payload.message_id)
                    await message.remove_reaction(key, member)
    
    async def scripts(self, panel, message_id, command):
        for key, value in panel.items():
            if message_id == value:
                server = key
        if server == 'arma':
            server = 'arma3server'
            if 'hc_' in command:
                server = 'arma3server-hc'
                command = command.split('_')[1]
            await self.poller('bash/arma', server, command)
        elif server == 'ww2':
            server = 'arma3server'
            if 'hc_' in command:
                server = 'arma3server-hc'
                command = command.split('_')[1]
            await self.poller('bash/ww2', server, command)
        elif server == 'minecraft':
            await self.poller('bash/minecraft', 'mcserver', command)

    async def poller(self, script, server, command):
        import subprocess
        import asyncio
        cmd = [script, server, command]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while output is not None:
            retcode = output.poll()
            if retcode is not None:
                return
            else:
                await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(ControlPanel(bot))