import discord
from discord.ext import commands
import aiohttp
import lxml
import re


class Affiliator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        message_lower = message.content.lower()
        if 'amazon' in message_lower:
            list_message = message_lower.split()
            list_links = [x for x in list_message if 'amazon' in x]
            list_asin = await self.grab_asin(list_links)
            if list_asin:
                await self.send_message(list_asin, message)

    async def grab_asin(self, list_links):
        list_asin = []
        for link in list_links:
            asin = re.search('(gp/|dp/|product/|asin/)([a-z0-9]{10})', link)
            if asin:
                list_asin.append(asin.group(2))
        return list_asin

    async def send_message(self, list_asin, message):
        for asin in list_asin:
            link_affiliate = f"https://www.amazon.com/exec/obidos/ASIN/{asin}/thecoolerse0c-20"
            message_embed = await self.get_title(link_affiliate)
            await message.channel.send(embed=message_embed)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def http(self, url):
        async with aiohttp.ClientSession() as session:
            source = await self.fetch(session, url)
            return source

    async def get_title(self, url):
        import ast
        source = await self.http(url)
        tree = lxml.html.fromstring(source)
        xpath = '//span[@id="productTitle"]/text()'
        raw_title = ast.literal_eval(str(tree.xpath(xpath)))
        title = raw_title[0].strip()
        return await self.embeder(title, url)

    async def embeder(self, title, url):
        em = discord.Embed(
            title='TCS Affiliate Link', description='[{}]({})'.format(title, url), color=0xff9900)
        return em


def setup(bot):
    bot.add_cog(Affiliator(bot))