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
        emojis = ['start', 'stop', 'restart', 'validate', 'update']
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
        for server_value, key, value in zip(server.values(), panel.keys(), panel.values()):
            print(server_value)
            print(key)
            print(value)
            text = await self.embeder(server_value['title'], server_value['url'], emojis)
            panel = await self.opener()
            try:
                msg = await channel.fetch_message(panel.get(value))
                await msg.edit(embed=text)
            except:
                print("Control panel message hasn't been made yet.")
                msg = await channel.send(embed=text)
                msg = panel[key]
                # for emoji in emojis:
                #     await msg.add_reaction(emoji=emoji)
        await self.closer(panel)

    async def embeder(self, server_title, server_url, emojis):
        desc = 'Use the following reactions to perform actions on the server. Your reaction will be removed once the action has completed.'
        foot = 'The bot will show as "typing" while the action is runnning.'
        commands = {
            'start' : {
                'name' : "{} starts the server".format(emojis[0]),
                'value' : ""
            },
            'stop' : {
                'name' : "{} stops the server".format(emojis[1]),
                'value' : ""
            },
            'restart' : {
                'name' : "{} restarts the server.".format(emojis[2]),
                'value' : "*Use when you're not sure if the server is stopped.*"
            },
            'validate' : {
                'name' : "{} validates server files.".format(emojis[3]),
                'value' : "*Used to troubleshoot the server files.*"
            },
            'update' : {
                'name' : "{} updates the server.".format(emojis[4]),
                'value' : ""
            }
        }
        em = discord.Embed(
            title=server_title, description=desc, color=0x008080)
        em.set_thumbnail(url=server_url)
        for value in commands.values():
            em.add_field(name=value['name'], value=value['value'], inline=True)
        em.set_footer(text=foot)
        return em

def setup(bot):
    bot.add_cog(ControlPanel(bot))