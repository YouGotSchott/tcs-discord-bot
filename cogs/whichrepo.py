import discord
from discord.ext import commands
from random import choice
from datetime import datetime
from pytz import timezone


class WhichRepo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        insults = [
            'big fucking idiot',
            'satchel of assholes',
            'absolute fucking dumpling',
            'cock weasel',
            'fucking sitzpinkler',
            'bumbling sycophant'
        ]
        dummy = message.author.mention
        msg = message.content.lower()
        if ('which repo' in msg \
        or 'what repo' in msg) \
        and datetime.now(timezone('US/Eastern')).weekday() in [2, 4, 5]:
            if str(message.author.id) == 188724792680120320:
                await message.send(
                    "{} We're using the main repo you {}.".format(dummy, 'crayon eater'))
            else:
                await message.send(
                    "{} We're using the main repo you {}.".format(dummy, choice(insults)))


def setup(bot):
    bot.add_cog(WhichRepo(bot))