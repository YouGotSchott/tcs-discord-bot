import discord
from discord.ext import commands


class HowTall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['whosefault'])
    async def whosfault(self, ctx, *args):
        helpers = discord.utils.get(self.bot.get_all_channels(), name="helpers")
        tcs_management = discord.utils.get(
            self.bot.get_all_channels(), name="tcs-management"
        )
        if (ctx.message.channel == helpers) or (ctx.message.channel == tcs_management):
            username = " ".join(args)
            yes, no = await self.find_voters(username)
            if not yes:
                await ctx.message.add_reaction("\U0001f44e")
                return
            em = await self.make_shame_message(yes, no, username)
            await ctx.send(embed=em)

    async def find_voters(self, username):
        results = await self.bot.conn.fetch(
            """
        SELECT applications_id, discord_user_id, is_yes
        FROM application_votes
        WHERE applications_id = (SELECT id FROM applications WHERE enjin_username = $1 );
        """,
            username,
        )
        yes = []
        no = []
        for x in results:
            guild = self.bot.get_guild(self.bot.guilds[0].id)
            member = guild.get_member(x["discord_user_id"])
            nickname = member.display_name
            if x["is_yes"]:
                yes.append(nickname)
            else:
                no.append(nickname)
        return yes, no

    async def make_shame_message(self, yes, no, username):
        yes_msg = "\u200B"
        no_msg = ""
        em = discord.Embed(title="Why is **{}** here?".format(username), color=0x5DBCD2)
        for x in yes:
            yes_msg += "{}\n".format(x)
        em.add_field(name="Blame these people:", value=yes_msg, inline=False)
        if no:
            for x in no:
                no_msg += "{}\n".format(x)
            em.add_field(name="These people knew better:", value=no_msg, inline=False)
            return em
        em.add_field(
            name="Apparently no one knew better",
            value="<:feelscornman:485958281458876416>",
            inline=False,
        )
        return em


def setup(bot):
    bot.add_cog(HowTall(bot))
