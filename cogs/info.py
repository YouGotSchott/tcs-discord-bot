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

    @commands.command()
    async def armaserver(self, ctx):
        em = discord.Embed(
            title="Arma Server - Direct Connect Info",
            description=f"```IP: {server_info['main_host']}\nPassword: {server_info['main_pass']}\nPort: {server_info['main_port']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @commands.command()
    async def testserver(self, ctx):
        em = discord.Embed(
            title="Mission Making Server - Direct Connect Info",
            description=f"```IP: {server_info['main_host']}\nPassword: {server_info['test_pass']}\nPort: {server_info['test_port']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @commands.command()
    async def mcserver(self, ctx):
        em = discord.Embed(
            title="Minecraft Server - Direct Connect Info",
            description=f"```IP: {server_info['mc_host']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @commands.command()
    async def ts3(self, ctx):
        em = discord.Embed(
            title="TS3 - Direct Connect Info",
            description=f"```{server_info['ts3']}```",
            color=0x383F35,
        )
        em.set_thumbnail(url=self.thumbnail)
        await ctx.channel.send(embed=em)

    @commands.command()
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
