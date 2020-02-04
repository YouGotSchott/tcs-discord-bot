from config import secret_amazon
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp
import lxml
import re
import bottlenose


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
            message_embed = await self.link_maker(asin)
            await message.channel.send(embed=message_embed)

    async def link_maker(self, asin):
        amazon = bottlenose.Amazon(
            secret_amazon['key'], 
            secret_amazon['secret'], 
            secret_amazon['tag'],
            Parser=lambda text: BeautifulSoup(text, 'lxml-xml'),
            MaxQPS=0.9)
        response = amazon.ItemLookup(ItemId=asin)
        title = response.find('Title').string
        link = response.find('DetailPageURL').string
        return await self.embeder(title, link)

    async def embeder(self, title, url):
        em = discord.Embed(
            title='TCS Affiliate Link', description='[{}]({})'.format(title, url), color=0xff9900)
        return em


def setup(bot):
    bot.add_cog(Affiliator(bot))