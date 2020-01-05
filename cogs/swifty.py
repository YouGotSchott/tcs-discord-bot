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
    async def unsung(self, ctx):
        await self.embeder(ctx, "unsung")

    async def embeder(self, ctx, repo):
        repo_url = "http://mods.thecoolerserver.com/"
        if "unsung" in repo:
            repo_url = "http://unsung.thecoolerserver.com/"
        swifty_guide = "https://www.thecoolerserver.com/wiki/m/39575060/page/Swifty#Mod_Installation"
        em = discord.Embed(
        title="Swifty Installation Guide", description="**__Repo URL__:**```{}```".format(repo_url), url=swifty_guide, color=0x29b585)
        await ctx.send(embed=em)

    @swifty.command()
    async def uninstall(self, ctx):
        guide = {
            'description' : "```Swifty requires extra steps to uninstall correctly, please complete all steps before re-installing.```",
            'step 1' : "Uninstall Swifty like any other program with *Programs and Features* in Windows.",
            'step 2' : """Delete the Swifty Folders from `%appdata%` and `%localappdata%`. *(You can copy and paste these values into "Run" `⊞Win + R` to find them quicker.*)""",
            'step 3' : "[Re-download and install Swifty](https://www.thecoolerserver.com/wiki/m/39575060/page/Swifty#Mod_Installation)"
        }
        em = discord.Embed(
            title="How to Uninstall Swifty 2.2.1", description=guide['description'], color=0x29b585)
        em.add_field(name="**STEP 1**", value=guide['step 1'], inline=True)
        em.add_field(name="**STEP 2**", value=guide['step 2'], inline=True)
        em.add_field(name="**STEP 3**", value=guide['step 3'], inline=True)
        await ctx.send(embed=em)

    @swifty.command()
    async def shortcut(self, ctx):
        guide = {
            'description' : "```Swifty may not create a shortcut on your desktop, and while some people use the downloaded *Installation File* as a way to open Swifty, it is not recommended and could cause unintentional side-effects.```",
            'step 1' : """Find the "Swifty.exe" at `%localappdata%\\Swifty\\app-2.2.1\\` *(You can copy and paste this directory into "Run" `⊞Win + R` to find it quicker.*).""",
            'step 2' : """Right-click "Swifty.exe" and choose "Send to Desktop"."""
        }
        em = discord.Embed(
            title="How to Create a Desktop Shortcut for Swifty", description=guide['description'], color=0x29b585)
        em.add_field(name="**STEP 1**", value=guide['step 1'], inline=True)
        em.add_field(name="**STEP 2**", value=guide['step 2'], inline=True)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Swifty(bot))