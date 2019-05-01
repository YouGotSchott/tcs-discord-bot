import discord
from discord.ext import commands
from pathlib import Path


class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.panel = str(Path('cogs/data/panel.json'))

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    async def opener(self):
        with open(self.panel, 'r') as f:
            return json.load(f)

    async def closer(self, panel):
        with open(self.panel, 'w') as f:
            json.dump(panel, f)

    async def msg_setup(self):
        channel = discord.utils.get(self.bot.get_all_channels(), name='control-panel')
        text = await self.embeder(emojis)
        panel = await self.opener()
        try:
            self.arma = await channel.fetch_message(panel.get('arma'))
            self.arma_hc = await channel.fetch_message(panel.get('arma_hc'))
            self.ww2 = await channel.fetch_message(panel.get('ww2'))
            self.ww2_hc = await channel.fetch_message(panel.get('ww2_hc'))
            await self.msg.edit(embed=text)
        except:
            print("Role Message hasn't been added yet")
            self.msg = await channel.send(embed=text)

    async def embeder(self, emojis):


def setup(bot):
    bot.add_cog(ControlPanel(bot))