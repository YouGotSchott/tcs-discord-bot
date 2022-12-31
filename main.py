import discord
from discord.ext import commands
from config import bot, TOKEN, secret_db, intents
import asyncpg
import asyncio
import aiohttp
import logging

async def create_db_pool():
    print("[DB] Attempting connection...")
    conn = await asyncpg.create_pool(
        host=secret_db['host'],
        database=secret_db['database'],
        user=secret_db['user'],
        password=secret_db['password'],
        port=secret_db['port'])
    print("[DB] Database connected.")
    return conn

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!',
                        case_insensitive=True,
                        intents=intents)
        self.initial_extensions = [
            'cogs.applications',
            'cogs.downloader',
            'cogs.nextnextop',
            'cogs.danceit',
            'cogs.briefing',
            'cogs.eject',
            'cogs.baconbuster',
            'cogs.swatter',
            'cogs.roleselector',
            'cogs.tasker',
            'cogs.attendance',
            'cogs.howtall',
            'cogs.giveaway',
            'cogs.swifty',
            'cogs.butler',
            'cogs.helpers',
            'cogs.grenade',
            'cogs.signup',
            'cogs.cleanup',
            'cogs.ping_abuse',
            'cogs.whitelist',
            'cogs.cooldown',
            'cogs.voice_clear',
            'cogs.whosfault',
            'cogs.info',
            'cogs.chance',
            'cogs.unit_patch'
        ]

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            try:
                await self.load_extension(ext)
            except Exception as error:
                print('{} cannot be loaded. [{}]'.format(ext, error))


    async def close(self):
        await super().close()
        await self.session.close()

async def run_bot():
    bot = MyBot()
    discord.utils.setup_logging()
    discord.utils.setup_logging(level=logging.INFO, root=False)
    async with bot:
        bot.conn = await create_db_pool()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(run_bot())