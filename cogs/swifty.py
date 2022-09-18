import discord
from discord.ext import commands
from random import randint
import asyncio


class Swifty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def swifty(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    @swifty.command()
    async def repo(self, ctx):
        await self.embeder(ctx)

    async def embeder(self, ctx):
        modern_url = "http://modern.thecoolerserver.com/"
        ww2_url = "http://ww2.thecoolerserver.com/"
        swifty_guide = "https://wiki.thecoolerserver.com/en/startup/swifty"
        em = discord.Embed(
            title="Swifty Installation Guide",
            description="**__Modern URL__:**```{}```\n**__WW2 URL__:**```{}```".format(
                modern_url, ww2_url
            ),
            url=swifty_guide,
            color=0x29B585,
        )
        await ctx.send(embed=em)

    @swifty.command()
    async def uninstall(self, ctx):
        guide = {
            "description": "```Swifty requires extra steps to uninstall correctly, please complete all steps before re-installing.```",
            "step 1": "Uninstall Swifty like any other program with *Programs and Features* in Windows.",
            "step 2": """Delete the Swifty Folders from `%appdata%` and `%localappdata%`. *(You can copy and paste these values into "Run" `⊞Win + R` to find them quicker.*)""",
            "step 3": "[Re-download and install Swifty](https://wiki.thecoolerserver.com/en/startup/swifty)",
        }
        em = discord.Embed(
            title="How to Uninstall Swifty 2.2.1",
            description=guide["description"],
            color=0x29B585,
        )
        em.add_field(name="**STEP 1**", value=guide["step 1"], inline=True)
        em.add_field(name="**STEP 2**", value=guide["step 2"], inline=True)
        em.add_field(name="**STEP 3**", value=guide["step 3"], inline=True)
        await ctx.send(embed=em)

    @swifty.command()
    async def shortcut(self, ctx):
        guide = {
            "description": "```Swifty may not create a shortcut on your desktop, and while some people use the downloaded *Installation File* as a way to open Swifty, it is not recommended and could cause unintentional side-effects.```",
            "step 1": """Find the "Swifty.exe" at `%localappdata%\\Swifty\\app-2.2.1\\` *(You can copy and paste this directory into "Run" `⊞Win + R` to find it quicker.*).""",
            "step 2": """Right-click "Swifty.exe" and choose "Send to Desktop".""",
        }
        em = discord.Embed(
            title="How to Create a Desktop Shortcut for Swifty",
            description=guide["description"],
            color=0x29B585,
        )
        em.add_field(name="**STEP 1**", value=guide["step 1"], inline=True)
        em.add_field(name="**STEP 2**", value=guide["step 2"], inline=True)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Swifty(bot))
