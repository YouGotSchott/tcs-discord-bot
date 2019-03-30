import discord


class Swatter:
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        if self.client.user in message.mentions:
            await self.client.add_reaction(message, '\U0001f5de')


def setup(client):
    client.add_cog(Swatter(client))
