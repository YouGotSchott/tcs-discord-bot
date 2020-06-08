import discord
from discord.ext import commands
import aiohttp
from config import secret_sftp
from pathlib import Path, PurePath
import asyncssh
import os


class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = PurePath('cogs/data/pbo_cache/')

    @commands.group()
    @commands.has_any_role('upload', 'admin', 'moderator')
    async def upload(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction('👎')

    @upload.command()
    async def main(self, ctx):
        self.folder = PurePath('\\MissionUpload\\Main\\')
        await self.downloader(ctx)

    @upload.command()
    async def test(self, ctx):
        self.folder = PurePath('\\MissionUpload\\Test\\')
        await self.downloader(ctx)

    async def downloader(self, ctx):
        await self.status_check(ctx, await self.ingest(ctx))  

    async def ingest(self, ctx):
        url = ctx.message.attachments[0].url
        filename = url.split("/")
        if filename[-1].endswith('.pbo'):
            self.end_file = PurePath(filename[-1])
            path = str(self.cache / self.end_file)
            attachment = {
                "url": url,
                "path": path
            }
            return attachment
        else:
            await ctx.send('ERROR: Invalid File Type')
            await ctx.message.add_reaction('👎')

    async def status_check(self, ctx, attachment):
        url = attachment["url"]
        path = attachment["path"]
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    await self.writer(ctx, path, r)
                    return
                else:
                    await ctx.send('ERROR: Network Error')
                    await ctx.message.add_reaction('👎')
                    return

    async def writer(self, ctx, path, r):
        with open(path, 'wb') as f:
            while True:
                chunk = await r.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        temp_name = PurePath(str(self.end_file).replace('.pbo', '.temp'))
        new_path = self.cache / temp_name
        os.rename(path, new_path)
        await self.sftp_to_server(new_path, temp_name)
        await ctx.message.add_reaction('👍')
        os.remove(new_path)

    async def sftp_to_server(self, new_path, temp_name):
        async with asyncssh.connect(host=secret_sftp['host'], 
                                    port=secret_sftp['port'], 
                                    username=secret_sftp['user'],
                                    client_keys=secret_sftp['client_key']) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.put(new_path, remotepath=self.folder)
                await sftp.rename(self.folder / temp_name, self.folder / self.end_file)


def setup(bot):
    bot.add_cog(Downloader(bot))
