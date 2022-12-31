import discord
from discord.ext import commands
import aiohttp
from lxml import html


class Briefing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target = (
            "https://www.thecoolerserver.com/forum/m/32181632/op/rss/forum_id/6725698"
        )

    @commands.command()
    async def briefing(self, ctx):
        url = await self.url_grab()
        await ctx.send(url)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self, url):
        async with aiohttp.ClientSession() as session:
            source = await self.fetch(session, url)
            return source

    async def url_grab(self):
        source = await self.main(self.target)
        tree = html.fromstring(source.encode("utf-8"))
        xpath = "/html/body/rss/channel/item[1]/text()"
        href = tree.xpath(xpath)
        for item in href:
            link = item.strip()
            if link:
                return link


async def setup(bot):
    await bot.add_cog(Briefing(bot))
