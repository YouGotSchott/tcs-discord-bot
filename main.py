import discord
from discord.ext import commands
from com.pbo_downloader import PBODownloader
from com.data.cues import cue_message
from config import client, TOKEN, main_path, ww2_path

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

@client.command(pass_context=True)
async def tism(ctx):
    await client.send_message(ctx.message.channel, cue_message)

@client.event
async def on_message(message):
    if client.user in message.mentions:
        await client.add_reaction(message, '\U0001f5de')
    msg = str(message.content)
    msg = msg.replace(" ", "")
    if message.author.id == '206380629523300352' \
        and msg.startswith('<:') \
        and msg.endswith('>'):
        await client.delete_message(message)
    await client.process_commands(message)

client.run(TOKEN)