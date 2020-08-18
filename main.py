import discord
from discord.ext import commands
from config import bot, TOKEN, secret_db
import asyncpg

bot.remove_command('help')

async def create_db_pool():
    print("[DB] Attempting connection...")
    bot.conn = await asyncpg.create_pool(
        host=secret_db['host'],
        database=secret_db['database'],
        user=secret_db['user'],
        password=secret_db['password'],
        port=secret_db['port'])
    print("[DB] Database connected.")

extensions = [
    'cogs.downloader',
    'cogs.nextnextop',
    'cogs.danceit',
    'cogs.briefing',
    'cogs.eject',
    'cogs.baconbuster',
    'cogs.swatter',
    'cogs.roleselector',
    'cogs.whichrepo',
    'cogs.tasker',
    'cogs.attendance',
    'cogs.howtall',
    'cogs.control_panel',
    'cogs.giveaway',
    'cogs.swifty',
    'cogs.butler',
    'cogs.helpers',
    'cogs.grenade',
    'cogs.signup',
    'cogs.cleanup',
    'cogs.countdown',
    'cogs.ping_abuse',
    'cogs.whitelist',
    'cogs.cooldown',
    'cogs.voice_clear'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    bot.loop.run_until_complete(create_db_pool())
    bot.run(TOKEN)
