import discord
from config import client
from textwrap import wrap
from com.data.dancing_alpha import dancing_alpha

async def dance_it_main(*args):
    output = ''
    for word in args:
        letters = ''
        for letter in word:
            if letter.isalpha():
                letter = letter.lower()
                letters += dancing_alpha[letter]
            else:
                letters += letter
        word = letters
        output += word
        output += '    '
    msgs = wrap(output, 2000)
    for msg in msgs:
        await client.say(msg)