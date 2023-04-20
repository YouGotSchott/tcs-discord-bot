import discord
from discord.ext import commands
import aiohttp
from config import secret_sftp, sftp_users, secret_paths
from pathlib import Path, PurePath
import asyncssh
import os


class Downloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = PurePath("cogs/data/pbo_cache/")

    @commands.group()
    @commands.has_any_role("upload", "admin", "moderator")
    async def upload(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    # Upload commands for the Modern Repo
    @upload.group()
    async def modern(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    @modern.command(name="main")
    async def modern_main(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["modern"]
        await self.downloader(ctx)

    @modern.command(name="test")
    async def modern_test(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["modern_test"]
        await self.downloader(ctx)

    # Upload commands for the Cold War Repo
    @upload.group()
    async def coldwar(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    @coldwar.command(name="main")
    async def coldwar_main(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["cwr"]
        await self.downloader(ctx)

    @coldwar.command(name="test")
    async def coldwar_test(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["cwr_test"]
        await self.downloader(ctx)

    # Upload commands for the WW2 Repo
    @upload.group()
    async def ww2(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    @ww2.command(name="main")
    async def ww2_main(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["ww2"]
        await self.downloader(ctx)

    @ww2.command(name="test")
    async def ww2_test(self, ctx):
        self.folder = PurePath(secret_paths["path"])
        self.sftp_user = sftp_users["ww2_test"]
        await self.downloader(ctx)

    async def downloader(self, ctx):
        await self.status_check(ctx, await self.ingest(ctx))

    async def ingest(self, ctx):
        url = ctx.message.attachments[0].url
        filename = url.split("/")
        if filename[-1].endswith(".pbo"):
            self.end_file = PurePath(filename[-1])
            path = str(self.cache / self.end_file)
            attachment = {"url": url, "path": path}
            return attachment
        else:
            await ctx.send("ERROR: Invalid File Type")
            await ctx.message.add_reaction("👎")

    async def status_check(self, ctx, attachment):
        url = attachment["url"]
        path = attachment["path"]
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    await self.writer(ctx, path, r)
                    return
                else:
                    await ctx.send("ERROR: Network Error")
                    await ctx.message.add_reaction("👎")
                    return

    async def writer(self, ctx, path, r):
        with open(path, "wb") as f:
            while True:
                chunk = await r.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        temp_name = PurePath(str(self.end_file).replace(".pbo", ".temp"))
        new_path = self.cache / temp_name
        os.rename(path, new_path)
        await self.sftp_to_server(new_path, temp_name)
        await ctx.message.add_reaction("👍")
        os.remove(new_path)

    async def sftp_to_server(self, new_path, temp_name):
        async with asyncssh.connect(
            host=secret_sftp["host"],
            port=secret_sftp["port"],
            username=self.sftp_user,
            client_keys=secret_sftp["client_key"],
        ) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.put(new_path, remotepath=self.folder)
                await sftp.rename(self.folder / temp_name, self.folder / self.end_file)


async def setup(bot):
    await bot.add_cog(Downloader(bot))
