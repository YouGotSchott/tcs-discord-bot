import discord
from discord.ext import commands
import aiohttp
import ast
from lxml import html


class Briefing:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def briefing(self, ctx):
        await self.rotation(ctx)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self):
        async with aiohttp.ClientSession() as session:
            source = await self.fetch(session,
                                      'https://www.thecoolerserver.com/forum/m/32181632/viewforum/6725698')
            return source

    async def url_grab(self, source):
        tree = html.fromstring(source)
        xpath = '//a[@class="thread-view"]/@href'
        href = tree.xpath(xpath)
        recent_briefing = ast.literal_eval(str(href))
        return "https://www.thecoolerserver.com" + str(recent_briefing[0])

    async def rotation(self, ctx):
        source = await self.main()
        url = await self.url_grab(source)
        await self.client.send_message(ctx.message.channel, url)


def setup(client):
    client.add_cog(Briefing(client))
