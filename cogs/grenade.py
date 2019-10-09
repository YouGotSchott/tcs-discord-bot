import discord
from discord.ext import commands
from random import randint
import asyncio
import itertools


class Grenade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toggle = False
        self.dive_toggle = False
        self.dive_messages = []

    @commands.command()
    async def grenade(self, ctx):
        await ctx.message.delete()
        self.bot_member = ctx.me
        self.blast = randint(4, 10)
        self.channel = ctx.channel
        self.post_messages = []
        self.toggle = True
        self.dive_toggle = True
        zone = await ctx.channel.history(limit=self.blast).flatten()
        count_msg = await ctx.send('\U0001f4a3 \U0001f55b')
        await self.countdown(count_msg)
        if self.dive_messages:
            for msg in self.dive_messages:
                await msg.add_reaction('\U0001f5de')
            self.toggle = False
            self.dive_toggle = False
            self.dive_messages.clear()
            return
        for pre, post in itertools.zip_longest(zone, self.post_messages):
            if post == count_msg:
                pass
            if pre == count_msg:
                pass
            await self.reactor(pre)
            if post:
                await self.reactor(post)
        self.toggle = False
        self.dive_toggle = False

    async def reactor(self, message):
        try:
            await message.add_reaction('\U0001f5de')
        except:
            pass
    
    async def countdown(self, count_msg):
        clocks = ['\U0001F550', '\U0001F551', '\U0001F552',
        '\U0001F553', '\U0001F554', '\U0001F555', '\U0001F556',
        '\U0001F557', '\U0001F558', '\U0001F559', '\U0001F55A']
        for clock in clocks:
            await asyncio.sleep(1)
            string = '\U0001f4a3 {}'.format(clock)
            await count_msg.edit(content=string)
        await asyncio.sleep(1)
        await count_msg.edit(content='\U0001f4a5', delete_after=10)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.toggle and \
        (len(self.post_messages) <= self.blast) and \
        (message.channel == self.channel):
            self.post_messages.append(message)

    @commands.command()
    async def dive(self, ctx):
        if self.dive_toggle:
            self.dive_messages.append(ctx.message)


def setup(bot):
    bot.add_cog(Grenade(bot))