import discord
from discord.ext import commands

amazon = {
    'description': '''
    🇺🇸 **US MEMEBERS ONLY** 🇺🇸
    Use the [Amazon Affiliate Link](https://www.amazon.com/?&_encoding=UTF8&tag=thecoolerse0c-20&linkCode=ur2&linkId=29b1e7ab218e7b0ef5e05f03199eb2b7&camp=1789&creative=9325) on your next purchase and the server recieves a percentage of the sale **AT NO COST TO YOU!** Make sure you *click the link* at least **24hrs before you check out**.
    ''',
    'title': 'Amazon Affiliate Link',
    'url': 'https://www.amazon.com/?&_encoding=UTF8&tag=thecoolerse0c-20&linkCode=ur2&linkId=29b1e7ab218e7b0ef5e05f03199eb2b7&camp=1789&creative=9325',
    'color': 0xff9900,
    'thumbnail': 'https://i.imgur.com/3W9MJpb.png',
    'footer': 'PRIVACY BADGER USERS: Ensure Privacy Badger is turned OFF while using the link'
}

class Links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def amazon(self, ctx):
        em = discord.Embed(
            title=amazon['title'], description=amazon['description'], url=amazon['url'], color=amazon['color'])
        em.set_thumbnail(url=amazon['thumbnail'])
        em.set_footer(text=amazon['footer'])
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Links(bot))
