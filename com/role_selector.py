import discord
import aiohttp
from config import client
from com.data import embeds


class RoleSelector:
    async def post(self, ctx, msg_data):
        em = discord.Embed(title=msg_data['title'], description=msg_data['description'], colour=0xDEADBF)
        em.set_author(name=msg_data['name'], icon_url=client.user.avatar_url)
        msg = await client.send_message(client.get_channel('557248486324699176'), embed=em)
        return msg

    async def dict_creator(self, title, description, name):
        msg_data = {
            'title' : title,
            'description' : description,
            'name' : name
        }
        return msg_data

    async def remove(self, msgs):
        if msgs:
            await client.delete_messages(msgs)

    async def rotation(self, ctx, msgs):
        await self.remove(msgs)
        embed_msgs = zip(embeds.titles, embeds.descriptions, embeds.names)
        for title, description, name in embed_msgs:
            msg_data = await self.dict_creator(title, description, name)
            msg = await self.post(ctx, msg_data)
            msgs.append(msg)
