import discord
import aiohttp
from config import client

class PBODownloader:
    async def downloader(self, ctx, file_path):
        await self.status_check(ctx, await self.ingest(ctx, file_path))

    async def ingest(self, ctx, file_path):
        url = ctx.message.attachments[0]['url']
        filename = url.split("/")
        if filename[-1].endswith('.pbo'):
            path = file_path + str(filename[-1])
            attachment = { 
                "url" : url,
                "path" : path
                }
            return attachment
        else:
            await client.send_message(ctx.message.channel,
            'ERROR: Invalid File Type')
            await client.add_reaction(ctx.message, '👎')

    async def status_check(self, ctx, attachment):
        url = attachment["url"]
        path = attachment["path"]
        async with aiohttp.get(url) as r:
                if r.status == 200:
                    await self.writer(ctx, path, r)
                    return
                else:
                    await client.send_message(ctx.message.channel,
                    'ERROR: Network Error')
                    await client.add_reaction(ctx.message, '👎')
                    return

    async def writer(self, ctx, path, r):
        with open(path, 'wb') as f:
            while True:
                chunk = await r.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
            await client.add_reaction(ctx.message, '👍')