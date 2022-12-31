import discord
from discord.ext import commands
import re


class UnitPatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def patchmedaddy(self, ctx, arg):
        user_data = {
            "steam_id": int(arg.strip()),
            "user_id": ctx.author.id,
            "nickname": ctx.author.display_name,
        }
        pattern = re.compile("^[0-9]{17}$")
        is_steam_id = pattern.match(str(user_data["steam_id"]))
        if not is_steam_id:
            await ctx.message.add_reaction("👎")
            return
        await self.check_db(user_data)
        if await self.check_db(user_data):
            await self.update_db(user_data)
        else:
            await self.add_to_db(user_data)
        await ctx.message.add_reaction("👍")

    async def check_db(self, user_data):
        return await self.bot.conn.fetchrow(
            """
        SELECT user_id FROM date_joined
        WHERE user_id = $1
        """,
            user_data["user_id"],
        )

    async def update_db(self, user_data):
        await self.bot.conn.execute(
            """
        UPDATE date_joined
        SET nickname = $2, steam_id = $3
        WHERE user_id = $1;
        """,
            user_data["user_id"],
            user_data["nickname"],
            user_data["steam_id"],
        )

    async def add_to_db(self, user_data):
        await self.bot.conn.execute(
            """
        INSERT INTO date_joined (user_id, nickname, steam_id)
        VALUES ($1, $2, $3);
        """,
            user_data["user_id"],
            user_data["nickname"],
            user_data["steam_id"],
        )


async def setup(bot):
    await bot.add_cog(UnitPatch(bot))
