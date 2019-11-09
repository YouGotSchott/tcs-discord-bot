import discord
from discord.ext import commands
from config import bot, wait
import asyncio
import psycopg2

class DBConn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        wait(self.bot.aconn)
        print("Database connected.")


def setup(bot):
    bot.add_cog(DBConn(bot))