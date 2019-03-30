import discord
from discord.ext import commands
from config import client, TOKEN

client.remove_command('help')

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
    'cogs.deploy'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
    client.run(TOKEN)
