import discord
from discord.ext import commands
from config import bot, TOKEN

bot.remove_command('help')

extensions = [
    'cogs.downloader',
    'cogs.nextnextop',
    'cogs.danceit',
    'cogs.briefing',
    'cogs.eject',
    'cogs.baconbuster',
    'cogs.swatter',
    'cogs.roleselector',
    'cogs.links',
    'cogs.scripts',
    'cogs.whichrepo',
    'cogs.affiliator',
    'cogs.tasker',
    'cogs.attendance'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    bot.run(TOKEN)
