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
        if 'bitch' in message.content.lower() and \
            message.author.id == 178960174738833409:
            await message.add_reaction('its_just_ham:504456342119907349')
    
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def newspaper_stacker(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.emoji) == '\U0001f5de':
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.add_reaction('\U0001f5de')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def ham_stacker(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji).strip('<:>') == 'its_just_ham:504456342119907349' \
            and message.author.id == 178960174738833409:
            guild = self.bot.get_guild(payload.guild_id)
            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.add_reaction('its_just_ham:504456342119907349')


def setup(bot):
    bot.add_cog(Swatter(bot))
