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
        if "ww2" in repo:
            em.set_footer(text="Check pinned messages in #ww2-repo for additional infomation")
        await ctx.send(embed=em)

    @swifty.command()
    async def uninstall(self, ctx):
        guide = {
            'description' : "```Swifty requires extra steps to uninstall correctly, please complete all steps before re-installing.```",
            'step 1' : "Uninstall Swifty like any other program with *Programs and Features* in Windows.",
            'step 2' : """Delete the Swifty Folders from `%appdata%` and `%localappdata%`. *(You can copy and paste these values into "Run" `⊞Win + R` to find them quicker.*)""",
            'step 3' : "[Re-download Swifty](https://s3.amazonaws.com/files.enjin.com/1015535/Swifty_2.2.1_Setup.zip) and re-install."
        }
        em = discord.Embed(
            title="How to Uninstall Swifty", description=guide['description'], color=0x29b585)
        em.add_field(name="**STEP 1**", value=guide['step 1'], inline=True)
        em.add_field(name="**STEP 2**", value=guide['step 2'], inline=True)
        em.add_field(name="**STEP 3**", value=guide['step 3'], inline=True)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Swifty(bot))