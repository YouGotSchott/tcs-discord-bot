import discord
from discord.ext import commands
from config import bot, secret_db
import asyncio
import asyncpg

class DBConn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Starting database connection...")
        self.bot.conn = await asyncpg.connect(
            host=secret_db['host'],
            database=secret_db['database'],
            user=secret_db['user'],
            password=secret_db['password'],
            port=secret_db['port'])
        print("Database connected.")


def setup(bot):
    bot.add_cog(DBConn(bot))