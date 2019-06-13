import discord
from discord.ext import commands


class Helpers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('admin', 'moderator', 'helper')
    async def removefng(self, ctx):
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        fng = discord.utils.get(guild.roles, name="fng")
        for user in ctx.message.mentions:
            member = guild.get_member(user.id)
            if fng not in member.roles:
                continue
            await member.remove_roles(fng)
        await ctx.message.add_reaction('👍')

def setup(bot):
    bot.add_cog(Helpers(bot))