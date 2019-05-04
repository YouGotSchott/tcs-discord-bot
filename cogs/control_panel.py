import discord
from discord.ext import commands
from pathlib import Path
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
        self.emojis = {
            '\U000025b6' : 'start',
            '\U000023f9' : 'stop',
            '\U0001f501' : 'restart',
            '\U0000002a\U000020e3' : 'validate',
            '\U00002b06' : 'update'
        }
        server = {
            'arma' : {
                'title' : 'ARMA 3 SERVER',
                'url' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
            },
            'arma_hc' : {
                'title' : 'ARMA 3 HEADLESS CLIENT',
                'url' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
            },
            'ww2' : {
                'title' : 'ARMA 3 WW2 SERVER',
                'url' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
            },
            'ww2_hc' : {
                'title' : 'ARMA 3 WW2 SERVER',
                'url' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
            },
            'minecraft' : {
                'title' : 'MINECRAFT',
                'url' : 'https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png'
            }
        }
        panel = await self.opener()
        if not panel.values():
            for key, value in server.items():
                print("Control panel message hasn't been made yet.")
                text = await self.embeder(value['title'], value['url'])
                msg = await channel.send(embed=text)
                panel[key] = msg.id
                for moji in self.emojis.keys():
                    await msg.add_reaction(emoji=moji)
        else:
            for p_value, p_key, s_value in zip(panel.values(), panel.keys(), server.values()):
                msg = await channel.fetch_message(p_value)
                text = await self.embeder(s_value['title'], s_value['url'])
                panel[p_key] = msg.id
                await msg.edit(embed=text)
        await self.closer(panel)
        self.panel_dict = await self.opener()

    async def embeder(self, server_title, server_url):
        desc = 'Use the following reactions to perform actions on the server. Your reaction will be removed once the action has completed.'
        foot = 'The bot will show as "typing" while the action is runnning.'
        commands = {
            'start' : "\U000025b6 Start the server",
            'stop' : "\U000023f9 Stop the server",
            'restart' : "\U0001f501 Restart the server",
            'validate' : "\U0000002a\U000020e3 Validate server files",
            'update' : "\U00002b06 Update the server"
        }
        em = discord.Embed(
            title=server_title, description=desc, color=0x008080)
        em.set_thumbnail(url=server_url)
        for value in commands.values():
            em.add_field(name=value, value="|", inline=False)
        em.set_footer(text=foot)
        return em

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def control_reaction(self, payload):
        if payload.message_id not in self.panel_dict.values():
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
            await self.poller('bash/arma', 'arma3server', command)
        elif server == 'arma_hc':
            await self.poller('bash/arma', 'arma3server-hc', command)
        elif server == 'ww2':
            await self.poller('bash/ww2', 'arma3server', command)
        elif server == 'ww2_hc':
            await self.poller('bash/ww2', 'arma3server-hc', command)
        elif server == 'minecraft':
            await self.poller('bash/minecraft', 'mcserver', command)
    
    async def poller(self, script, server, command):
        from subprocess import Popen
        p = Popen([script, server, command])
        retcode = p.poll()
        while True:
            if retcode is not None:
                return
            else:
                continue

def setup(bot):
    bot.add_cog(ControlPanel(bot))