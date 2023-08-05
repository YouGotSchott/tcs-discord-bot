import discord
from discord.ext import commands
from formio_api import FormioWrapper
import textwrap
from datetime import datetime, timedelta, timezone
import asyncio
from gspread_api import GoogleHelperSheet
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import urllib
from config import sendgrid


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
            await self.app_handler()

    async def every_five_minutes(self, current):
        while True:
            output = current + (datetime.min - current) % timedelta(minutes=5)
            return (output - current).seconds

    async def app_handler(self):
        token = await FormioWrapper().login()
        app_ids = await FormioWrapper().get_application_list(token)
        app_ids = await self.compare_app_lists(app_ids)
        if app_ids:
            for app in app_ids:
                user_data = await FormioWrapper().get_application_info(token, app)
                if user_data is None:
                    continue
                await self.write_to_database(user_data)
                db_user_data = await self.get_user_data(app=app)
                msg = await self.app_channel.send(
                    embed=await self.generate_app_message(db_user_data)
                )
                await self.update_msg_id(msg, app)
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
        await FormioWrapper().logout()

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
                            [user_data["formio_username"]]
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
        SELECT formio_app_id FROM applications;
        """
        )
        result_vals = [x["formio_app_id"] for x in result]
        app_ids = [x for x in app_ids if x not in result_vals]
        return app_ids

    async def update_msg_id(self, msg, app):
        await self.bot.conn.execute(
            """
            UPDATE applications SET message_id = $1
            WHERE formio_app_id = $2;
            """,
            msg.id,
            app,
        )

    async def get_user_data(self, app=False, msg=False):
        if app:
            result = await self.bot.conn.fetchrow(
                """
            SELECT * FROM applications WHERE formio_app_id = $1;
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
                INSERT INTO applications (formio_app_id, time_created, user_ip, formio_username, age, time_zone, is_wednesday, is_friday, is_saturday, steam_profile, referral, reason, member_referral, other_referral, email)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                """,
            user_data["application_id"],
            user_data["created"],
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
            user_data["member_referral"],
            user_data["other_referral"],
            user_data["email"],
        )

    async def generate_app_message(self, user_data, approved=False, declined=False):
        referral = user_data["referral"]
        ref = {
            'reddit' : 'Reddit',
            'youtube': 'YouTube',
            'arma3Units' : 'Arma 3 Units',
            'currentMember': 'currentMember',
            'other': 'other'
        }
        referral = ref[referral]
        if user_data["member_referral"]:
            referral = user_data["member_referral"]
        if user_data["other_referral"]:
            referral = user_data["other_referral"]
        em_color = 0xDBA51F
        if approved:
            em_color = 0x0A6003
        if declined:
            em_color = 0x991313
        em = discord.Embed(
            title=str(user_data["formio_username"]),
            description="**Created:** {}\n**Age:** {}\n**Time Zone:** {}\n\n[Steam Account]({})\n".format(
                await self.localize_time(user_data["time_created"]),
                user_data["age"],
                user_data["time_zone"],
                user_data["steam_profile"].replace('_', r'\_').strip(),
            ),
            color=em_color,
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
        em.add_field(name="How did you find us?", value=referral, inline=False)
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
                name="Tell us about yourself.", value=user_data["reason"], inline=False
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
        if availability["wednesday"]:
            wed = True
        if availability["friday"]:
            fri = True
        if availability["saturday"]:
            sat = True
        return wed, fri, sat

    async def localize_time(self, utc_dt):
        utc_time = utc_dt.replace(tzinfo=timezone.utc)
        utc_timestamp = round(utc_time.timestamp())
        return f"<t:{utc_timestamp}:F>"


class ReactionHandler:
    def __init__(self, bot):
        self.bot = bot

    async def thumbs_up_reaction_add(self, msg, payload):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_down_user_list = [usr async for usr in thumbs_down.users()]
        thumbs_down_users = [x.id for x in thumbs_down_user_list if not x.bot]
        if payload.user_id in thumbs_down_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction("\U0001f44e", user)
        return thumbs_up.count

    async def thumbs_down_reaction_add(self, msg, payload):
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_up_user_list = [usr async for usr in thumbs_up.users()]
        thumbs_up_users = [x.id for x in thumbs_up_user_list if not x.bot]
        if payload.user_id in thumbs_up_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction("\U0001f44d", user)
        return thumbs_down.count

    async def add_vote(self, msg):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == "\U0001f44d"][0]
        thumbs_up_user_list = [usr async for usr in thumbs_up.users()]
        thumbs_up_users = [x.id for x in thumbs_up_user_list if not x.bot]
        val = True
        for user in thumbs_up_users:
            await self.write_votes_to_db(msg, user, val)
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == "\U0001f44e"][0]
        thumbs_down_user_list = [usr async for usr in thumbs_down.users()]
        thumbs_down_users = [x.id for x in thumbs_down_user_list if not x.bot]
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
            approved_names += "\n{}".format(user["formio_username"])
        for user in denied:
            denied_names += "\n{}".format(user["formio_username"])
        return ".\nTo be Approved:\n{}\n\nTo be Denied:\n{}".format(
            approved_names, denied_names
        )

    async def check_approved_status(self):
        results = await self.bot.conn.fetch(
            """
        SELECT formio_app_id, formio_username, is_message_sent, is_staged FROM applications
        WHERE is_approved IS NULL;
        """
        )

        for result in results:
            if result["is_staged"] is None:
                await self.fill_is_staged(result)

        results = await self.bot.conn.fetch(
            """
        SELECT formio_app_id, formio_username, is_staged, email FROM applications
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
        WHERE formio_app_id = $2;
        """,
            value,
            result["formio_app_id"],
        )

    async def fill_is_approved(self, result):
        if not result["is_staged"]:
            value = False
        else:
            value = True
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_approved = $1
        WHERE formio_app_id = $2;
        """,
            value,
            result["formio_app_id"],
        )

    async def set_approved(self, ctx, arg):
        await self.bot.conn.execute(
            """
        UPDATE applications SET is_staged = $1
        WHERE formio_username = $2
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
        WHERE formio_username = $2
        AND is_approved IS NULL;
        """,
            False,
            arg,
        )
        await ctx.message.add_reaction("👍")

    async def start_approval(self, ctx):
        approved, denied = await self.check_approved_status()
        for user in denied:
            with open("declined_msg.html", "r") as f:
                message = f.read()
            await self.send_email(user["email"], message, is_approved=False)
            await self.fill_is_approved(user)
        for user in approved:
            invite_link = await self.generate_invite(user["formio_username"])
            with open("approved_msg.html", "r") as f:
                message = f.read()
            message = message.replace(r"{{discord_invite}}", str(invite_link))
            await self.send_email(user["email"], message)
            await self.fill_is_approved(user)

        await ctx.message.add_reaction("👍")

    async def send_email(self, email, message, is_approved=True):
        sendgrid_client = SendGridAPIClient(api_key=sendgrid["key"])

        from_email = Email(sendgrid["sender"])
        to_email = To(email)
        subject = "Welcome to The Cooler Server!"
        if not is_approved:
            subject = "A message from The Cooler Server"
        content = Content("text/html", message)

        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()
        try:
            response = sendgrid_client.client.mail.send.post(request_body=mail_json)
            if response.status_code < 300:
                print(f"Email sent to {email}: {response.status_code}")
        except urllib.error.HTTPError as e:
            e.read()

    async def generate_invite(self, username):
        channel_rules = discord.utils.get(self.bot.get_all_channels(), name="rules")
        return await channel_rules.create_invite(
            reason=f"Created invite link for {username}", max_age=2_592_000, max_uses=0
        )


async def setup(bot):
    await bot.add_cog(Applications(bot))
