import discord
from random import choice
from datetime import datetime


class WhichRepo:
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        insults = [
            'big fucking idiot',
            'satchel of assholes',
            'absolute fucking dumpling',
            'cock weasel'
        ]
        dummy = message.author.mention
        msg = message.content.lower()
        if 'which repo' in msg \
        or 'what repo' in msg \
        and datetime.today().weekday() in [2, 5, 6]:
            await self.client.send_message(message.channel, 
            "{} We're using the main repo you {}.".format(dummy, choice(insults)))


def setup(client):
    client.add_cog(WhichRepo(client))