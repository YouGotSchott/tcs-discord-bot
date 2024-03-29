import discord
from discord.ext import commands


class Swatter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await message.add_reaction('\U0001f5de')
        if 'skynet' in message.content.lower():
            await message.add_reaction('\U0001f916')
    
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def newspaper_stacker(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.emoji) == '\U0001f5de':
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.add_reaction('\U0001f5de')


async def setup(bot):
    await bot.add_cog(Swatter(bot))
