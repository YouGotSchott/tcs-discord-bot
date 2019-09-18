import discord
from discord.ext import commands
import aiohttp
from lxml import html
import re


class Affiliator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        if 'www.amazon.com' in msg:
            print(msg)
            try:
                product_code = await self.dp_check(msg)
            except:
                product_code = await self.prod_check(msg)
            print(product_code)
            url = "https://www.amazon.com/exec/obidos/ASIN/{}/thecoolerse0c-20".format(product_code)
            print(url)
            try:
                em = await self.title_grab(url)
                await message.channel.send(embed=em)
            except Exception as e:
                print(e)
                return
        else:
            return

    async def dp_check(self, msg):
        try:
            product = re.search('/dp/(.*)/', msg)
            product_code = product.group(1).upper()
        except:
            product = msg.split('/dp/', 1)[-1]
            product_code = product.upper()
        return product_code

    async def prod_check(self, msg):
        try:
            product = re.search('/product/(.*)/', msg)
            product_code = product.group(1).upper()
        except:
            product = msg.split('/product/', 1)[-1]
            product_code = product.upper()
        return product_code
    
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def http(self, url):
        async with aiohttp.ClientSession() as session:
            source = await self.fetch(session, url)
            return source
    
    async def title_grab(self, url):
        import ast
        source = await self.http(url)
        tree = html.fromstring(source)
        xpath = '//span[@id="productTitle"]//text()'
        raw_title = ast.literal_eval(str(tree.xpath(xpath)))
        print(raw_title)
        title = raw_title[0].strip()
        return await self.embeder(title, url)
    
    async def embeder(self, title, url):
        em = discord.Embed(
            title='TCS Affiliate Link', description='[{}]({})'.format(title, url), color=0xff9900)
        return em


def setup(bot):
    bot.add_cog(Affiliator(bot))