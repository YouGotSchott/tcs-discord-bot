import discord
from discord.ext import commands
import aiohttp
from config import main_path, ww2_path
from pathlib import Path


class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role('upload', 'admin', 'moderator')
    async def upload(self, ctx):
        await self.downloader(ctx, main_path)

    @commands.command()
    @commands.has_any_role('upload', 'admin', 'moderator')
    async def ww2upload(self, ctx):
        await self.downloader(ctx, ww2_path)

    async def downloader(self, ctx, file_path):
        await self.status_check(ctx, await self.ingest(ctx, file_path))

    async def ingest(self, ctx, file_path):
        url = ctx.message.attachments[0].url
        filename = url.split("/")
        if filename[-1].endswith('.pbo'):
            end_file = Path(filename[-1])
            path = str(file_path / end_file)
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
            await ctx.message.add_reaction('👍')


def setup(bot):
    bot.add_cog(Downloader(bot))
