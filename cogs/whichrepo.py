import discord
from discord.ext import commands
from random import choice
from datetime import datetime
from pytz import timezone
import re


class WhichRepo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = re.sub(r'\s+', '', message.content.lower())
        if ('whichrepo' in msg \
        or 'whatrepo' in msg):
            if datetime.now(timezone('US/Eastern')).weekday() in [2, 4, 5]:
                await self.insult(message, 'main')
            else:
                await message.add_reaction('\U0001f5de')

    async def insult(self, message, repo):
        dummy = message.author.mention
        insults = [
            'big fucking idiot',
            'satchel of assholes',
            'absolute fucking dumpling',
            'cock weasel',
            'fucking sitzpinkler',
            'bumbling sycophant',
            'leaky fuck faucet',
            'ignorant ingrown sausage link',
            'absolute pinecone',
            'incompetent inkless pen',
            'unintelligent park bench',
            'dense cabbage',
            'Canadian',
            'badly packed parachute'
        ]
        if message.author.id == 188724792680120320:
            insults.append('crayon eater')
        await message.channel.send(
            "{} We're using the {} repo you {}.".format(dummy, repo, choice(insults)))


async def setup(bot):
    await bot.add_cog(WhichRepo(bot))