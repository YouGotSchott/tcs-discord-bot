import discord
from discord.ext import commands


class Helpers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('admin', 'moderator', 'helper')
    async def trained(self, ctx):
        guild = self.bot.get_guild(self.bot.guilds[0].id)
        untrained = discord.utils.get(guild.roles, name="untrained")
        if not ctx.message.mentions:
            await ctx.message.add_reaction('👎')
            return
        for user in ctx.message.mentions:
            member = guild.get_member(user.id)
            if untrained not in member.roles:
                continue
            await member.remove_roles(untrained)
        await ctx.message.add_reaction('👍')

def setup(bot):
    bot.add_cog(Helpers(bot))