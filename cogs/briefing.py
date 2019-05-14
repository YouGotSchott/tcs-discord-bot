import discord
from discord.ext import commands
import aiohttp
import ast
from lxml import html


class Briefing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def briefing(self, ctx):
        await self.rotation(ctx)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self):
        async with aiohttp.ClientSession() as session:
            source = await self.fetch(session,
                'https://www.thecoolerserver.com/forum/m/32181632/op/rss/forum_id/6725698')
            return source

    async def url_grab(self, source):
        tree = html.fromstring(source.encode('utf-8'))
        xpath = '/html/body/rss/channel/item[1]/text()'
        href = tree.xpath(xpath)
        for item in href:
            check = item.strip()
            if check:
                link = check
                continue
        return link

    async def rotation(self, ctx):
        source = await self.main()
        url = await self.url_grab(source)
        await ctx.send(url)


def setup(bot):
    bot.add_cog(Briefing(bot))
