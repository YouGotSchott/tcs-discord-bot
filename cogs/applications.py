import discord
from discord.ext import commands
from enjin_api import EnjinWrapper
import textwrap
from datetime import datetime, timedelta
import pytz
import asyncio


class ApplicationException(Exception):
    pass

class Applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.app_channel = discord.utils.get(self.bot.get_all_channels(), name='applications')
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
                msg = await self.app_channel.send(embed=await self.generate_app_message(db_user_data))
                await self.update_msg_id(msg, int(app))
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def app_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        if payload.channel_id == self.app_channel.id:
            if str(payload.emoji) == '\U0001f44d':
                msg = await self.app_channel.fetch_message(payload.message_id)
                thumbs_up_count = await ReactionHandler(self.bot).thumbs_up_reaction_add(msg, payload)
                if thumbs_up_count >= 11:
                    message_sent = await ReactionHandler(self.bot).check_if_message_sent(msg)
                    if message_sent is None:
                        await ReactionHandler(self.bot).add_vote(msg)
                        await ReactionHandler(self.bot).send_ts3_invite(msg.id)
                        await ReactionHandler(self.bot).set_message_status(msg.id, approved=True)
                        user_data = await self.get_user_data(msg=msg.id)
                        await msg.edit(embed=await self.generate_app_message(user_data, approved=True))
                        
            if str(payload.emoji) == '\U0001f44e':
                msg = await self.app_channel.fetch_message(payload.message_id)
                thumbs_down_count = await ReactionHandler(self.bot).thumbs_down_reaction_add(msg, payload)
                if thumbs_down_count >= 11:
                    message_sent = await ReactionHandler(self.bot).check_if_message_sent(msg)
                    if message_sent is None:
                        await ReactionHandler(self.bot).add_vote(msg)
                        await ReactionHandler(self.bot).set_message_status(msg.id)
                        user_data = await self.get_user_data(msg=msg.id)
                        await msg.edit(embed=await self.generate_app_message(user_data, declined=True))


    async def compare_app_lists(self, app_ids):
        result = await self.bot.conn.fetch(
        """
        SELECT enjin_app_id FROM applications;
        """
        )
        result_vals = [x['enjin_app_id'] for x in result]
        app_ids = [x for x in app_ids if int(x) not in result_vals]
        return app_ids

    async def update_msg_id(self, msg, app):
        await self.bot.conn.execute(
            """
            UPDATE applications SET message_id = $1
            WHERE enjin_app_id = $2;
            """,
            msg.id,
            app
        )

    async def get_user_data(self, app=False, msg=False):
        if app:
            result = await self.bot.conn.fetchrow(
            """
            SELECT * FROM applications WHERE enjin_app_id = $1;
            """,
            app
            )
            return result
        if msg:
            result = await self.bot.conn.fetchrow(
            """
            SELECT * FROM applications WHERE message_id = $1;
            """,
            msg
            )
            return result
        raise ApplicationException('No identifier defined')

    async def write_to_database(self, user_data):
        wed, fri, sat = await self.availability_convert(user_data['availability'])
        await self.bot.conn.execute(
                """
                INSERT INTO applications (enjin_app_id, time_created, enjin_user_id, user_ip, enjin_username, age, time_zone, is_wednesday, is_friday, is_saturday, steam_profile, referral, reason)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                user_data['application_id'],
                user_data['created'],
                user_data['user_id'],
                user_data['user_ip'],
                user_data['username'],
                user_data['age'],
                user_data['time_zone'],
                wed,
                fri,
                sat,
                user_data['steam_account'],
                user_data['referral'],
                user_data['reason']
            )

    async def generate_app_message(self, user_data, approved=False, declined=False):
        em_color = 0xDBA51F
        if approved:
            em_color = 0x0A6003
        if declined:
            em_color = 0x991313
        em = discord.Embed(
            title=str(user_data['enjin_username']),
            description="**Created:** {}\n**Age:** {}\n**Time Zone:** {}\n\n[Steam Account]({})\n".format(await self.localize_time(user_data['time_created']), user_data['age'], user_data['time_zone'], user_data['steam_profile']),
            color=em_color,
            url="https://www.thecoolerserver.com/dashboard/applications/application?app_id={}".format(user_data['enjin_app_id']),
        )
        em.add_field(
            name="Availability",
            value=await self.availability_checks(user_data['is_wednesday'], user_data['is_friday'], user_data['is_saturday']),
            inline=False,
        )
        em.add_field(
            name="How did you find us?", value=user_data['referral'], inline=False
        )
        if len(user_data['reason']) > 1024:
            em.add_field(
                name="Why do you want to join?",
                value=textwrap.shorten(
                    user_data['reason'], width=1024, placeholder="..."
                ),
                inline=False,
            )
        else:
            em.add_field(
                name="Why do you want to join?", value=user_data['reason'], inline=False
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
        return "> {} **Wednesday**\n> {} **Friday**\n> {} **Saturday**".format(wed, fri, sat)

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
                date_today
            )
            return
        await self.bot.conn.execute(
            """
            UPDATE enjin SET session_id = $1, date_created = $2
            WHERE id = 1;
            """,
            session_id,
            date_today
        )

class ReactionHandler:
    def __init__(self, bot):
        self.bot = bot

    async def thumbs_up_reaction_add(self, msg, payload):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == '\U0001f44d'][0]
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == '\U0001f44e'][0]
        thumbs_down_users = [x.id for x in await thumbs_down.users().flatten() if not x.bot]
        if payload.user_id in thumbs_down_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction('\U0001f44e', user)
        return thumbs_up.count

    async def thumbs_down_reaction_add(self, msg, payload):
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == '\U0001f44e'][0]
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == '\U0001f44d'][0]
        thumbs_up_users = [x.id for x in await thumbs_up.users().flatten() if not x.bot]
        if payload.user_id in thumbs_up_users:
            user = self.bot.guilds[0].get_member(payload.user_id)
            await msg.remove_reaction('\U0001f44d', user)
        return thumbs_down.count

    async def removed_reaction(self):
        await self.bot.conn.execute(
        """
        DELETE FROM roles WHERE attendance_id = (SELECT id FROM attendance WHERE attendance.user_id = $1 
        AND attendance.date = $2)
        """, 
        user_id, 
        self.date)

    async def add_vote(self, msg):
        thumbs_up = [x for x in msg.reactions if str(x.emoji) == '\U0001f44d'][0]
        thumbs_up_users = [x.id for x in await thumbs_up.users().flatten() if not x.bot]
        val = True
        for user in thumbs_up_users:
            await self.write_votes_to_db(msg, user, val)
        thumbs_down = [x for x in msg.reactions if str(x.emoji) == '\U0001f44e'][0]
        thumbs_down_users = [x.id for x in await thumbs_down.users().flatten() if not x.bot]
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
        val
    )

    async def check_if_message_sent(self, message):
        result = await self.bot.conn.fetchrow(
            """
        SELECT is_message_sent FROM applications WHERE message_id = $1;
        """,
        message.id
        )
        return result['is_message_sent']

    async def send_ts3_invite(self, message_id):
        result = await self.bot.conn.fetchrow(
            """
        SELECT enjin_user_id FROM applications WHERE message_id = $1;
        """,
        message_id
        )
        session_id = await SessionHanlder(self.bot).test_session_id()
        title = 'Application Received!'
        body = """In the meantime come join our TeamSpeak and say hello.
        It’s not required, but highly encouraged.\n\n
        TS Address: ts3.thecoolerserver.com
        """
        await EnjinWrapper().send_message(session_id, title, body, [15473358])

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
        message_id
    )

def setup(bot):
    bot.add_cog(Applications(bot))
