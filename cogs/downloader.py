import discord
from discord.ext import commands
import aiohttp
from config import ftp_host, ftp_user, ftp_pwd
from pathlib import Path


class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = Path('cogs/data/pbo_cache/')

    @commands.group()
    @commands.has_any_role('upload', 'admin', 'moderator')
    async def upload(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction('👎')

    @upload.command()
    async def main(self, ctx):
        self.folder = 'main_mpmissions'
        await self.downloader(ctx)

    @upload.command()
    async def unsung(self, ctx):
        self.folder = 'unsung_mpmissions'
        await self.downloader(ctx)

    @upload.command()
    async def test(self, ctx):
        self.folder = 'test_mpmissions'
        await self.downloader(ctx)

    async def downloader(self, ctx):
        await self.status_check(ctx, await self.ingest(ctx))  

    async def ingest(self, ctx):
        url = ctx.message.attachments[0].url
        filename = url.split("/")
        if filename[-1].endswith('.pbo'):
            self.end_file = Path(filename[-1])
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
        await self.ftp_to_server(path)
        await ctx.message.add_reaction('👍')

    async def ftp_to_server(self, path):
        import ftplib
        import os
        ftp = ftplib.FTP(host=ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_pwd)
        ftp.cwd(self.folder)
        filename = str(self.end_file)
        with open(path, 'rb') as data_file:
            ftp.storbinary("STOR " + filename, data_file)
            ftp.close()
        os.remove(path)


def setup(bot):
    bot.add_cog(Downloader(bot))
