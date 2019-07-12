import discord
from discord.ext import commands
import asyncio


class Signup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startsingup(self, ctx):
        # Creates a fake !startsignup command
        self.bot.fake_toggle = True
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        evreyone = discord.utils.get(guild.roles, name="evreyone")
        await ctx.send("{} Roster signup for tonight's operation is now live!  Please use the !role command to submit your desired roles to the roster. https://docs.google.com/spreadsheets/d/1ObWkVSrXvUjron4Q9hK6Fy_sYWE1b-w135A7CPGfwBs".format(evreyone.mention))


def setup(bot):
    bot.add_cog(Signup(bot))
