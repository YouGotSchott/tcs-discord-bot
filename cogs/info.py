import discord
from discord.ext import commands
import aiohttp
from config import server_info


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = (
            "https://s3.amazonaws.com/files.enjin.com/1015535/site_logo/2020_logo.png"
        )

    @commands.group()
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.add_reaction("👎")

    # Modern Info
    @info.group()
    async def modern(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Modern Arma Server - Direct Connect Info",
                description=f"```IP: {server_info['main_host']}\nPassword: {server_info['main_pass']}\nPort: {server_info['modern_port']}```",
                color=0x383F35,
            )
            em.set_thumbnail(url=self.thumbnail)
            await ctx.channel.send(embed=em)

    @modern.command(name="test")
    async def modern_test(self, ctx):
        em = discord.Embed(
            title="Modern Mission Making Server - Direct Connect Info",
            description=f"```IP: {server_info['main_host']}\nPassword: {server_info['test_pass']}\nPort: {server_info['modern_test_port']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    # Cold War Info
    @info.group()
    async def coldwar(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="Cold War Arma Server - Direct Connect Info",
                description=f"```IP: {server_info['main_host']}\nPassword: {server_info['main_pass']}\nPort: {server_info['cw_port']}```",
                color=0x383F35,
            )
            em.set_thumbnail(url=self.thumbnail)
            await ctx.channel.send(embed=em)

    @coldwar.command(name="test")
    async def coldwar_test(self, ctx):
        em = discord.Embed(
            title="Cold War Mission Making Server - Direct Connect Info",
            description=f"```IP: {server_info['main_host']}\nPassword: {server_info['test_pass']}\nPort: {server_info['cw_test_port']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    # WW2 Info
    @info.group()
    async def ww2(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(
                title="World War II Arma Server - Direct Connect Info",
                description=f"```IP: {server_info['main_host']}\nPassword: {server_info['main_pass']}\nPort: {server_info['ww2_port']}```",
                color=0x383F35,
            )
            em.set_thumbnail(url=self.thumbnail)
            await ctx.channel.send(embed=em)

    @ww2.command(name="test")
    async def ww2_test(self, ctx):
        em = discord.Embed(
            title="World War II Mission Making Server - Direct Connect Info",
            description=f"```IP: {server_info['main_host']}\nPassword: {server_info['test_pass']}\nPort: {server_info['ww2_test_port']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @info.command()
    async def minecraft(self, ctx):
        em = discord.Embed(
            title="Minecraft Server - Direct Connect Info",
            description=f"```IP: {server_info['mc_host']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @info.command()
    async def ts3(self, ctx):
        em = discord.Embed(
            title="TS3 - Direct Connect Info",
            description=f"```{server_info['ts3']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @info.command()
    async def ocap(self, ctx):
        em = discord.Embed(
            title="OCAP URL",
            description=f"```{server_info['ocap']}```",
            color=0x383F35,
            url=server_info["ocap"],
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)


def setup(bot):
    bot.add_cog(Info(bot))
