import discord
from discord.ext import commands
from datetime import datetime, timedelta, date
from textwrap import wrap
from pytz import timezone


class NextNextOp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        msg = str(message.content)
        com_msg = msg.split(" ", 2)
        if com_msg[0].lower().startswith('!nextnext') \
                and com_msg[0].lower().endswith('op'):
            await self.next_next_op(com_msg[0], message.channel)

    async def date_converter(self):
        d = datetime.now(timezone('US/Eastern'))
        t = d.strftime('%m-%d-%Y')
        date_parse = t + ' 21:00:00'
        date = datetime.strptime(date_parse, '%m-%d-%Y %H:%M:%S')
        eastern = timezone('US/Eastern')
        return eastern.localize(date)

    async def counter(self, date, index):
        check = 0
        while check != index:
            if date.weekday() in [2, 4, 5]:
                if datetime.now(timezone('US/Eastern')) > date:
                    date = date + timedelta(days=1)
                check += 1
                if check == index:
                    break
                date = date + timedelta(days=1)
            else:
                date = date + timedelta(days=1)
        out = date - datetime.now(timezone('US/Eastern'))
        return out, date

    async def output(self, out, index, date, channel):
        if date.weekday() == 2:
            out_text = ("Next " * index) + "Operation: Wednesday Wars!  Starts in " + str(out.days) + " days, " + str(
                out.seconds // 3600) + " hours, and " + str((out.seconds // 60) % 60) + " minutes. Every Wednesday at 9PM EST/EDT."
        elif date.weekday() == 4:
            out_text = ("Next " * index) + "Operation: Training Ops.  Starts in " + str(out.days) + " days, " + str(
                out.seconds // 3600) + " hours, and " + str((out.seconds // 60) % 60) + " minutes. Every Friday at 9PM EST/EDT."
        elif date.weekday() == 5:
            out_text = ("Next " * index) + "Operation: Saturday Night Ops!  Starts in " + str(out.days) + " days, " + str(out.seconds // 3600) + \
                " hours, and " + str((out.seconds // 60) % 60) + \
                " minutes. Every Saturday at 9PM EST/EDT with signups starting at 8PM EST/EDT."
        msgs = wrap(out_text, 2000)
        for msg in msgs:
            await channel.send(msg)

    async def next_next_op(self, nextop, channel):
        index = nextop.count('next')
        date = await self.date_converter()
        out, out_date = await self.counter(date, index)
        await self.output(out, index, out_date, channel)


def setup(bot):
    bot.add_cog(NextNextOp(bot))
