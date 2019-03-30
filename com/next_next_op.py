import discord
from config import client
from datetime import datetime, timedelta, date
from textwrap import wrap


async def date_converter():
    d = datetime.today()
    t = d.strftime('%m-%d-%Y')
    date_parse = t + ' 21:00:00'
    date = datetime.strptime(date_parse, '%m-%d-%Y %H:%M:%S')
    return date


async def counter(date, index):
    check = 0
    while check != index:
        if date.weekday() in [2, 4, 5]:
            if datetime.today() > date:
                date = date + timedelta(days=1)
            check += 1
            if check == index:
                break
            date = date + timedelta(days=1)
        else:
            date = date + timedelta(days=1)
    out = date - datetime.today()
    return out, date


async def output(out, index, date, channel):
    if date.weekday() == 2:
        out_text = ("Next " * index) + "Operation: Wednesday Wars!  Starts in " + str(out.days) + " days, " + str(out.seconds // 3600) + " hours, and " + str((out.seconds // 60) % 60) + " minutes. Every Wednesday at 9PM EST/EDT."
    elif date.weekday() == 4:
        out_text = ("Next " * index) + "Operation: Training Ops.  Starts in " + str(out.days) + " days, " + str(out.seconds // 3600) + " hours, and " + str((out.seconds // 60) % 60) + " minutes. Every Friday at 9PM EST/EDT."
    elif date.weekday() == 5:
        out_text = ("Next " * index) + "Operation: Saturday Night Ops!  Starts in " + str(out.days) + " days, " + str(out.seconds // 3600) + " hours, and " + str((out.seconds // 60) % 60) + " minutes. Every Saturday at 9PM EST/EDT with signups starting at 8PM EST/EDT."
    msgs = wrap(out_text, 2000)
    for msg in msgs:
        await client.send_message(channel, msg)


async def next_next_main(nextop, channel):
    index = nextop.count('next')
    date = await date_converter()
    out, out_date = await counter(date, index)
    await output(out, index, out_date, channel)
