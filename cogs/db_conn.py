import discord
from discord.ext import commands
from config import bot
import asyncio
import psycopg2

class DBConn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.wait(bot.aconn)
        print("Database connected.")

    def wait(self, conn):
        import select
        while True:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [])
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [])
            else:
                raise psycopg2.OperationalError("poll() returned %s" % state)


def setup(bot):
    bot.add_cog(DBConn(bot))