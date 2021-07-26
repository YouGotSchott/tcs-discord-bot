import discord
from discord.ext import commands
from enjin_api import EnjinWrapper
import textwrap
from datetime import datetime, timedelta
import pytz
import asyncio
from gspread_api import GoogleHelperSheet


class ApplicationException(Exception):
    pass


class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_any_role("admin")
    async def apps(self, ctx):
        pass

    @apps.command()
    @commands.has_any_role("admin")
    async def getlist(self, ctx):
        msg = await Approver(self.bot).approve_check()
        await ctx.send(msg)

    @apps.command()
    @commands.has_any_role("admin")
    async def setapproved(self, ctx, *args):
        if args[0]:
            await Approver(self.bot).set_approved(ctx, args[0])
        else:
            await ctx.message.add_reaction("👎")

    @apps.command()
    @commands.has_any_role("admin")
    async def setdenied(self, ctx, *args):
        if args[0]:
            await Approver(self.bot).set_denied(ctx, args[0])
        else:
            await ctx.message.add_reaction("👎")

    @apps.command()
    @commands.has_any_role("admin")
    async def startapproval(self, ctx):
        await Approver(self.bot).start_approval(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        self.app_channel = discord.utils.get(
            self.bot.get_all_channels(), name="applications"
        )
        while True:
            sleep_time = await self.every_five_minutes(datetime.now())
            await asyncio.sleep(sleep_time)
            await self.app_hanlder()

    async def every_five_minutes(self, current):
        while True:
            output = current + (datetime.min - current) % timedelta(minutes=5)
            return (output - current).seconds

    async def app_hanlder(self):
        session_id = await SessionHanlder(self.bot).test_session_id()
        app_ids = await EnjinWrapper().get_application_list(session_id, "open")
        app_ids = await self.compare_app_lists(app_ids)
        if app_ids:
            for app in app_ids:
                user_data = await EnjinWrapper().get_application_info(session_id, app)
                if user_data is None:
                    continue
                await self.write_to_database(user_data)
                db_user_data = await self.get_user_data(app=int(app))
                msg = await self.app_channel.send(
                    embed=await self.generate_app_message(db_user_data)
                )
                await self.update_msg_id(msg, int(app))
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def app_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.channel_id == self.app_channel.id:
            if str(payload.emoji) == "\U0001f44d":
                msg = await self.app_channel.fetch_message(payload.message_id)
                thumbs_up_count = await ReactionHandler(
                    self.bot
                ).thumbs_up_reaction_add(msg, payload)
                if thumbs_up_count >= 10:
                    message_sent = await ReactionHandler(
                        self.bot
                    ).check_if_message_sent(msg)
                    if message_sent is None:
                        await ReactionHandler(self.bot).add_vote(msg)
                        await ReactionHandler(self.bot).send_ts3_invite(msg.id)
                        await ReactionHandler(self.bot).set_message_status(
                            msg.id, approved=True
                        )
                        user_data = await self.get_user_data(msg=msg.id)
                        await msg.edit(
                            embed=await self.generate_app_message(
                                user_data, approved=True
                            )
                        )
                        await GoogleHelperSheet().update_helper_sheet(
                            [user_data["enjin_username"]]
                        )

            if str(payload.emoji) == "\U0001f44e":
                msg = await self.app_channel.fetch_message(payload.message_id)
                thumbs_down_count = await ReactionHandler(
                    self.bot
                ).thumbs_down_reaction_add(msg, payload)
                if thumbs_down_count >= 10:
                    message_sent = await ReactionHandler(
                        self.bot
                    ).check_if_message_sent(msg)
                    if message_sent is None:
                        await ReactionHandler(self.bot).add_vote(msg)
                        await ReactionHandler(self.bot).set_message_status(msg.id)
                        user_data = await self.get_user_data(msg=msg.id)
                        await msg.edit(
                            embed=await self.generate_app_message(
                                user_data, declined=True
                            )
                        )

    async def compare_app_lists(self, app_ids):
        result = await self.bot.conn.fetch(
            """
        SELECT enjin_app_id FROM applications;
        """
        )
        result_vals = [x["enjin_app_id"] for x in result]
        app_ids = [x for x in app_ids if int(x) not in result_vals]
        return app_ids

    async def update_msg_id(self, msg, app):
        await self.bot.conn.execute(
            """
            UPDATE applications SET message_id = $1
            WHERE enjin_app_id = $2;
            """,
            msg.id,
            app,
        )

    async def get_user_data(self, app=False, msg=False):
        if app:
            result = await self.bot.conn.fetchrow(
                """
            SELECT * FROM applications WHERE enjin_app_id = $1;
            """,
                app,
            )
            return result
        if msg:
            result = await self.bot.conn.fetchrow(
                """
            SELECT * FROM applications WHERE message_id = $1;
            """,
                msg,
            )
            return result
        raise ApplicationException("No identifier defined")

    async def write_to_database(self, user_data):
        wed, fri, sat = await self.availability_convert(user_data["availability"])
        await self.bot.conn.execute(
            """
                INSERT INTO applications (enjin_app_id, time_created, enjin_user_id, user_ip, enjin_username, age, time_zone, is_wednesday, is_friday, is_saturday, steam_profile, referral, reason)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
            user_data["application_id"],
            user_data["created"],
            user_data["user_id"],
            user_data["user_ip"],
            user_data["username"],
            user_data["age"],
            user_data["time_zone"],
            wed,
            fri,
            sat,
            user_data["steam_account"],
            user_data["referral"],
            user_data["reason"],
        )

    async def generate_app_message(self, user_data, approved=False, declined=False):
        em_color = 0xDBA51F
        if approved:
            em_color = 0x0A6003
        if declined:
            em_color = 0x991313
        em = discord.Embed(
            title=str(user_data["enjin_username"]),
            description="**Created:** {}\n**Age:** {}\n**Time Zone:** {}\n\n[Steam Account]({})\n".format(
                await self.localize_time(user_data["time_created"]),
                user_data["age"],
                user_data["time_zone"],
                user_data["steam_profile"],
            ),
            color=em_color,
            url="https://www.thecoolerserver.com/dashboard/applications/application?app_id={}".format(
                user_data["enjin_app_id"]
            ),
        )
        em.add_field(
            name="Availability",
            value=await self.availability_checks(
                user_data["is_wednesday"],
                user_data["is_friday"],
                user_data["is_saturday"],
            ),
            inline=False,
        )
        em.add_field(
            name="How did you find us?", value=user_data["referral"], inline=False
        )
        if len(user_data["reason"]) > 1024:
            em.add_field(
                name="Why do you want to join?",
                value=textwrap.shorten(
                    user_data["reason"], width=1024, placeholder="..."
                ),
                inline=False,
            )
        else:
            em.add_field(
                name="Why do you want to join?", value=user_data["reason"], inline=False
            )
        return em

    async def availability_checks(self, data_wed, data_fri, data_sat):
        wed = "\U0001f6ab"
        fri = "\U0001f6ab"
        sat = "\U0001f6ab"
        if data_wed:
            wed = "\U00002705"
        if data_fri:
            fri = "\U00002705"
        if data_sat:
            sat = "\U00002705"
        return "> {} **Wednesday**\n> {} **Friday**\n> {} **Saturday**".format(
            wed, fri, sat
        )

    async def availability_convert(self, availability):
        wed = False
        fri = False
        sat = False
        if "Wednesday" in availability:
            wed = True
        if "Friday" in availability:
            fri = True
        if "Saturday" in availability:
            sat = True
        return wed, fri, sat

    async def localize_time(self, utc_dt):
        tz = pytz.timezone("America/New_York")
        return utc_dt.astimezone(tz).strftime("%Y-%m-%d @ %I:%M %p (ET)")


class SessionHanlder:
    def __init__(self, bot):
        self.bot = bot

    async def test_session_id(self):
        result = await self.bot.conn.fetchrow(
            """
        SELECT session_id, date_created FROM enjin WHERE id = 1;
        """
        )
        if not result:
            session_id = await EnjinWrapper().login()
            await self.update_record(session_id, created=False)
            return session_id
        session_id, date_created = result
        date_today = datetime.now().date()
        if (date_today - date_created).days > 7:
            session_id = await EnjinWrapper().login()
            await self.update_record(session_id)
            return session_id
        return session_id

    async def update_record(self, session_id, created=True):
        date_today = datetime.now().date()
        if not created:
            await self.bot.conn.execute(
                """
                INSERT INTO enjin (session_id, date_created)
                VALUES ($1, $2)
                """,
                session_id,
                date_today,
            )
            return
        await self.bot.conn.execute(
            """
            UPDATE enjin SET session_id = $1, date_created = $2
            WHERE id = 1;
            """,
            session_id,
            date_today,
        )


class ReactionHandler:
    def __init__(self, bot):
        self.bot = bot

    async def thumbs_up_reaction_add(self, msg, payload):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_down_users = [
            x.id for x in await thumbs_down.users().flatten() if not x.bot
        ]
        if payload.user_id in thumbs_down_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction("\U0001f44e", user)
        return thumbs_up.count

    async def thumbs_down_reaction_add(self, msg, payload):
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_up_users = [x.id for x in await thumbs_up.users().flatten() if not x.bot]
        if payload.user_id in thumbs_up_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction("\U0001f44d", user)
        return thumbs_down.count

    async def removed_reaction(self):
        await self.bot.conn.execute(
            """
        DELETE FROM roles WHERE attendance_id = (SELECT id FROM attendance WHERE attendance.user_id = $1 
        AND attendance.date = $2)
        """,
            user_id,
            self.date,
        )

    async def add_vote(self, msg):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_up_users = [x.id for x in await thumbs_up.users().flatten() if not x.bot]
        val = True
        for user in thumbs_up_users:
            await self.write_votes_to_db(msg, user, val)
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_down_users = [
            x.id for x in await thumbs_down.users().flatten() if not x.bot
        ]
        val = False
        for user in thumbs_down_users:
            await self.write_votes_to_db(msg, user, val)

    async def write_votes_to_db(self, message, user_id, val):
        if not user_id:
            return
        await self.bot.conn.execute(
            """
        INSERT INTO application_votes (applications_id, discord_user_id, is_yes)
        VALUES  ((SELECT id FROM applications WHERE message_id = $1), $2, $3);
        """,
            message.id,
            user_id,
            val,
        )

    async def check_if_message_sent(self, message):
        result = await self.bot.conn.fetchrow(
            """
        SELECT is_message_sent FROM applications WHERE message_id = $1;
        """,
            message.id,
        )
        return result["is_message_sent"]

    async def send_ts3_invite(self, message_id):
        result = await self.bot.conn.fetchrow(
            """
        SELECT enjin_user_id FROM applications WHERE message_id = $1;
        """,
            message_id,
        )
        session_id = await SessionHanlder(self.bot).test_session_id()
        title = "Application Received!"
        body = """In the meantime come join our TeamSpeak and say hello.
        It’s not required, but highly encouraged.\n\n
        TS Address: ts3.thecoolerserver.com
        """
        await EnjinWrapper().send_message(
            session_id, title, body, [result["enjin_user_id"]]
        )

    async def set_message_status(self, message_id, approved=False):
        val = False
        if approved:
            val = True
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_message_sent = $1
        WHERE message_id = $2;
        """,
            val,
            message_id,
        )


class Approver:
    def __init__(self, bot):
        self.bot = bot

    async def approve_check(self):
        approved, denied = await self.check_approved_status()
        approved_names = ""
        denied_names = ""
        for user in approved:
            approved_names += "\n{}".format(user["enjin_username"])
        for user in denied:
            denied_names += "\n{}".format(user["enjin_username"])
        return ".\nTo be Approved:\n{}\n\nTo be Denied:\n{}".format(
            approved_names, denied_names
        )

    async def check_approved_status(self):
        results = await self.bot.conn.fetch(
            """
        SELECT enjin_user_id, enjin_username, is_message_sent, is_staged FROM applications
        WHERE is_approved IS NULL;
        """
        )

        for result in results:
            if result["is_staged"] is None:
                await self.fill_is_staged(result)

        results = await self.bot.conn.fetch(
            """
        SELECT enjin_user_id, enjin_username, enjin_app_id, is_staged FROM applications
        WHERE is_approved IS NULL;
        """
        )
        approved = [x for x in results if x["is_staged"]]
        declined = [x for x in results if not x["is_staged"]]
        return approved, declined

    async def fill_is_staged(self, result):
        if not result["is_message_sent"]:
            value = False
        else:
            value = True
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_staged = $1
        WHERE enjin_user_id = $2;
        """,
            value,
            result["enjin_user_id"],
        )

    async def fill_is_approved(self, result):
        if not result["is_staged"]:
            value = False
        else:
            value = True
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_approved = $1
        WHERE enjin_user_id = $2;
        """,
            value,
            result["enjin_user_id"],
        )

    async def set_approved(self, ctx, arg):
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_staged = $1
        WHERE enjin_username = $2
        AND is_approved IS NULL;
        """,
            True,
            arg,
        )
        await ctx.message.add_reaction("👍")

    async def set_denied(self, ctx, arg):
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_staged = $1
        WHERE enjin_username = $2
        AND is_approved IS NULL;
        """,
            False,
            arg,
        )
        await ctx.message.add_reaction("👍")

    async def start_approval(self, ctx):
        with open("approved_message.txt", "r") as f:
            approval_message = f.read()
        session_id = await SessionHanlder(self.bot).test_session_id()

        approved, denied = await self.check_approved_status()
        denied_apps = [x["enjin_app_id"] for x in denied]
        await EnjinWrapper().decline_applications(session_id, denied_apps)
        for user in denied:
            await self.fill_is_approved(user)
        for user in approved:
            await EnjinWrapper().approve_applications(
                session_id, [user["enjin_app_id"]]
            )
            await EnjinWrapper().send_message(
                session_id,
                "Welcome to The Cooler Server!",
                approval_message,
                [user["enjin_user_id"]],
            )
            await self.fill_is_approved(user)
            await asyncio.sleep(30)
        await ctx.message.add_reaction("👍")


def setup(bot):
    bot.add_cog(Applications(bot))
