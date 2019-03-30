import discord
from discord.ext import commands
from random import randint


class Eject:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def eject(self, ctx):
        username = ctx.message.author.display_name
        luck = randint(1, 20)
        if luck == 20:
            await self.client.say("*{} hit the canopy on the way out!*".format(username))
            user_id = ctx.message.server.get_member(ctx.message.author.id)
            await self.client.kick(user_id)
        else:
            await self.client.say("*has kicked {} from the server!*".format(username))


def setup(client):
    client.add_cog(Eject(client))
