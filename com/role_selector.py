import discord
import aiohttp
from config import client

class RoleSelector:
    async def post(self, embed):
        client.send_message(
            client.get_channel('557248486324699176'),
            embed)
    
    async def remove(self):
        mgs = []
        async for x in client.logs_from(client.get_channel('557248486324699176'), limit = 100):
            mgs.append(x)
        await client.delete_messages(mgs)