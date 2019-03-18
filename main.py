import discord
from discord.ext import commands
from com.pbo_downloader import PBODownloader
from secret import client, TOKEN, main_path, ww2_path

client.remove_command('help')

@client.command(pass_context=True)
@commands.has_any_role('upload', 'admin', 'moderator')
async def upload(ctx):
    pbo = PBODownloader()
    await pbo.downloader(ctx, main_path)

@client.command(pass_context=True)
@commands.has_any_role('upload', 'admin', 'moderator')
async def uploadww2(ctx):
    pbo = PBODownloader()
    await pbo.downloader(ctx, ww2_path)

@client.event
async def on_message(message):
    if client.user in message.mentions:
        await client.add_reaction(message, '\U0001f5de')
    await client.process_commands(message)

client.run(TOKEN)