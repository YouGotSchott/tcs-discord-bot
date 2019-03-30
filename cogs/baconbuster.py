import discord


class BaconBuster:
    def __init__(self, client):
        self.client = client

    async def on_message(self, message):
        msg = str(message.content)
        msg = msg.replace(" ", "")
        if message.author.id == '206380629523300352' \
                and msg.startswith('<:') \
                and msg.endswith('>'):
            await self.client.delete_message(message)


def setup(client):
    client.add_cog(BaconBuster(client))
