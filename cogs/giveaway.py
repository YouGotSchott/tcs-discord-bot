import discord
from discord.ext import commands
from random import choice


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def giveaway(self, ctx):
        management = discord.utils.get(self.bot.get_all_channels(), name='tcs-management')
        if ctx.message.channel != management:
            return
        contestants = ctx.message.guild.members
        winner = choice(contestants).display_name
        msg = await self.embeder(winner)
        await ctx.send(embed=msg)

    async def embeder(self, winner):
        server_url = "https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2019_logo.png"
        em = discord.Embed(
            title="**__TCS GIVEAWAY WINNER__**", description="*for the random garbage giveaway...*", color=0x008080)
        em.set_thumbnail(url=server_url)
        em.add_field(name="☝🏼**{}** 😩💯💦👌🏼🔥🙏".format(winner), value="```Or just run it again because who fucking cares? No one else can see this.```", inline=False)
        em.set_footer(text="Terms and Conditions Apply")
        return em

def setup(bot):
    bot.add_cog(Giveaway(bot))