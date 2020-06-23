import discord
from discord.ext import commands
from async_mcrcon import MinecraftClient
from config import minecraft_rcon


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whitelist(self, ctx, *args):
        user_data = {
            'username' : args[0].strip().lower(),
            'user_id' : ctx.author.id,
            'nickname' : ctx.author.display_name
        }
        self.ctx = ctx
        await self.check_username(user_data)

    async def check_username(self, user_data):
        check_username_presence = await self.bot.conn.fetchrow("""
            SELECT mc_username FROM date_joined WHERE mc_username = $1
            AND NOT user_id = $2;
            """, user_data['username'], user_data['user_id'])
        if check_username_presence:
            await self.ctx.send(f"""Username "{user_data['username']}" already in use.""")
            return
        check_id = await self.bot.conn.fetchrow("""
            SELECT user_id FROM date_joined WHERE user_id = $1;
            """, user_data['user_id'])
        if not check_id:
            await self.bot.conn.execute("""
                INSERT INTO date_joined (user_id, nickname, mc_username)
                VALUES ($1, $2, $3)
                """, user_data['user_id'], user_data['nickname'], user_data['username'])
            await self.add_whitelist(user_data['username'])
        else:
            check_mc_username = await self.bot.conn.fetchrow("""
            SELECT mc_username FROM date_joined WHERE user_id = $1;
            """, user_data['user_id'])

            if check_mc_username[0] != user_data['username']:
                await self.bot.conn.execute("""
                    UPDATE date_joined SET mc_username = $2
                    WHERE user_id = $1
                    """, user_data['user_id'], user_data['username'])
                await self.remove_whitelist(check_mc_username[0])
                await self.add_whitelist(user_data['username'])
            else:
                await self.add_whitelist(user_data['username'])

    async def add_whitelist(self, username):
        async with MinecraftClient(minecraft_rcon['host'], minecraft_rcon['port'], minecraft_rcon['password']) as mc:
            output = await mc.send(f'whitelist add {username}')
        await self.ctx.send(f'Adding "{username}" to Whitelist => {output}')

    async def remove_whitelist(self, username):
        async with MinecraftClient(minecraft_rcon['host'], minecraft_rcon['port'], minecraft_rcon['password']) as mc:
            output = await mc.send(f'whitelist remove {username}')
        await self.ctx.send(f'Removing "{username}" from Whitelist => {output}')


def setup(bot):
    bot.add_cog(Whitelist(bot))