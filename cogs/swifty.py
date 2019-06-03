import discord
from discord.ext import commands


class Swifty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def swifty(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction('👎')

    @swifty.command()
    async def main(self, ctx):
        await self.embeder(ctx, "main")

    @swifty.command()
    async def ww2(self, ctx):
        await self.embeder(ctx, "ww2")

    async def embeder(self, ctx, repo):
        repo_url = "http://mods.thecoolerserver.com/"
        if "ww2" in repo:
            repo_url = "http://ww2.thecoolerserver.com/"
        swifty_guide = "https://www.thecoolerserver.com/forum/m/32181632/viewthread/27537251-tcs-swifty-installation-guide"
        em = discord.Embed(
        title="Swifty Installation Guide", description="**__Repo URL__:**```{}```".format(repo_url), url=swifty_guide, color=0x29b585)
        # em.set_thumbnail(url=amazon['thumbnail'])
        if "ww2" in repo:
            em.set_footer(text="Check pinned information in #ww2-repo for additional info")
        await ctx.send(embed=em)




def setup(bot):
    bot.add_cog(Swifty(bot))