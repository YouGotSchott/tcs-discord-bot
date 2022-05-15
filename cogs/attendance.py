import discord
from discord.ext import commands
from pytz import timezone
from datetime import datetime
from config import bot
import asyncio
from gspread_api import GoogleHelperSheet
from cogs.briefing import Briefing


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toggle = False

    @commands.command()
    @commands.has_any_role("admin", "moderator")
    async def startsignup(self, ctx):
        self.guild = self.bot.get_guild(self.bot.guilds[0].id)
        self.attending_role = await self.guild.create_role(
            name="attending", mentionable=True
        )
        self.bot.fake_toggle = False
        self.uid_list = []
        self.toggle = True
        await self.send_signup_message(ctx)
        await asyncio.sleep(5400)
        self.toggle = False
        self.uid_list.clear()
        await self.send_shutdown_message(ctx)

    @commands.command()
    @commands.has_any_role("admin", "moderator")
    async def stopsignup(self, ctx):
        self.toggle = False
        self.uid_list.clear()

    @commands.command()
    @commands.has_any_role("admin", "moderator")
    async def pausesignup(self, ctx):
        self.toggle = False

    @commands.command()
    @commands.has_any_role("admin", "moderator")
    async def resumesignup(self, ctx):
        self.toggle = True

    @commands.command()
    async def roll(self, ctx):
        if self.toggle == False:
            return
        with open("cogs/data/stupid_town.gif", "rb") as f:
            stupid_town = discord.File(f)
            await ctx.send(f"{ctx.message.author.mention}", file=stupid_town)

    @commands.command(aliases=["signup"])
    async def role(self, ctx, *args):
        if self.bot.fake_toggle == True:
            await self.fake_signup(ctx)
        if self.toggle == False:
            return
        fng = discord.utils.get(self.guild.roles, name="fng")
        if fng in ctx.message.author.roles:
            await ctx.message.add_reaction("👎")
            return
        uid = ctx.message.author.id
        if uid in self.uid_list:
            await ctx.message.add_reaction("👎")
            return
        roles = []
        for arg in args:
            roles.append(arg.replace(",", "").strip(" "))
        if len(roles) == 0:
            roles = [""]
        roles = roles[slice(0, min(3, len(roles)))]
        self.date = datetime.now(timezone("US/Eastern"))
        user_data = {
            "user_id": ctx.message.author.id,
            "nickname": ctx.message.author.display_name,
            "date": self.date,
            "roles": roles,
        }
        await self.writer(user_data)
        await self.write_to_sheet(user_data["nickname"], roles)
        self.uid_list.append(uid)
        await ctx.message.author.add_roles(self.attending_role)
        await ctx.message.add_reaction("👍")

    async def writer(self, user_data):
        await self.bot.conn.execute(
            """
        INSERT INTO attendance (user_id, nickname, date)
        VALUES ($1, $2, $3)
        """,
            user_data["user_id"],
            user_data["nickname"],
            user_data["date"],
        )
        for role in user_data["roles"]:
            await self.bot.conn.execute(
                """
            INSERT INTO roles (attendance_id, role)
            VALUES ((SELECT id FROM attendance WHERE attendance.user_id = $1 
            AND attendance.date = $2), $3)
            """,
                user_data["user_id"],
                user_data["date"],
                role,
            )

    async def write_to_sheet(self, user_name, roles):
        roles.insert(0, user_name)
        roles.insert(0, "0")
        await GoogleHelperSheet().update_roster(roles)

    @commands.command()
    @commands.has_any_role("admin", "moderator")
    async def remove(self, ctx):
        if self.toggle == False:
            return
        user_id = ctx.message.mentions[0].id
        await self.bot.conn.execute(
            """
        DELETE FROM roles WHERE attendance_id = (SELECT id FROM attendance WHERE attendance.user_id = $1 
        AND attendance.date = $2)
        """,
            user_id,
            self.date,
        )
        await self.bot.conn.execute(
            """
        DELETE FROM attendance WHERE user_id = $1
        AND date = $2""",
            user_id,
            self.date,
        )
        self.uid_list.remove(user_id)
        member = self.guild.get_member(user_id)
        if self.attending_role in member.roles:
            await member.remove_roles(self.attending_role)
        await ctx.message.add_reaction("👍")

    async def fake_signup(self, ctx):
        user = ctx.author
        role = discord.utils.get(user.guild.roles, name="silenced")
        await user.add_roles(role)
        await asyncio.sleep(30)
        await user.remove_roles(role)

    async def send_signup_message(self, ctx):
        em = discord.Embed(
            title="Saturday Signup Started!",
            description="[Link to Roster](https://docs.google.com/spreadsheets/d/1ObWkVSrXvUjron4Q9hK6Fy_sYWE1b-w135A7CPGfwBs) | [Link to Briefing]({})".format(
                await Briefing(self.bot).url_grab()
            ),
            color=0x008080,
        )
        em.set_thumbnail(
            url="https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2020_logo.png"
        )
        em.add_field(
            name="How to Sign Up",
            value="> The **!role** command parses on spaces; __replace your spaces with underscores!__\n```!role Squad_Lead, Team_Lead, Marksman```",
        )
        em.set_footer(text="Please respect the bot and sign up slowly!")
        await ctx.send("@everyone", embed=em)

    async def send_shutdown_message(self, ctx):
        em = discord.Embed(
            title="Saturday Signup Ended",
            description="> Signup has concluded; no more roles will be accepted.",
            color=0xFF0000,
        )
        em.set_thumbnail(
            url="https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2020_logo.png"
        )
        await ctx.send(embed=em)

    @commands.command()
    async def joined(self, ctx):
        user_id = ctx.author.id
        result = await self.bot.conn.fetchrow(
            """
        SELECT join_date FROM date_joined WHERE user_id = $1;
        """,
            user_id,
        )
        if not result:
            await ctx.message.add_reaction("👎")
            return
        joined_date = result[0].strftime("%d %B, %Y")
        await ctx.send(joined_date)

    @commands.command()
    async def nolife(self, ctx):
        result = await self.bot.conn.fetchrow(
            """
        SELECT COUNT(date) FROM attendance WHERE user_id = $1;
        """,
            ctx.author.id,
        )
        if result["count"] < 1:
            await ctx.send("You haven't attended any Saturday Ops.")
        else:
            await ctx.send("Saturday Op Count: {}".format(result["count"]))

    @commands.command()
    async def roster(self, ctx):
        em = discord.Embed(
            title="Command Roster 2 Electric Boogaloo(oo)",
            description="[Link to Roster](https://docs.google.com/spreadsheets/d/1ObWkVSrXvUjron4Q9hK6Fy_sYWE1b-w135A7CPGfwBs) | [Link to Briefing]({})".format(
                await Briefing(self.bot).url_grab()
            ),
            color=0x2A8947,
        )
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Attendance(bot))
