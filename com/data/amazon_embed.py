import discord
from config import client

msg_description = '''
🇺🇸 **US MEMEBERS ONLY** 🇺🇸
Use the [Amazon Affiliate Link](https://www.amazon.com/?&_encoding=UTF8&tag=thecoolerse0c-20&linkCode=ur2&linkId=29b1e7ab218e7b0ef5e05f03199eb2b7&camp=1789&creative=9325) on your next purchase and the server recieves a percentage of the sale **AT NO COST TO YOU!** Make sure you *click the link* at least **24hrs before you check out**.
'''

amazon_embed = discord.Embed(title='Amazon Affiliate Link', description=msg_description, url='https://www.amazon.com/?&_encoding=UTF8&tag=thecoolerse0c-20&linkCode=ur2&linkId=29b1e7ab218e7b0ef5e05f03199eb2b7&camp=1789&creative=9325', color=0xff9900)
amazon_embed.set_thumbnail(url='https://i.imgur.com/3W9MJpb.png')
amazon_embed.set_footer(text='PRIVACY BADGER USERS: Ensure Privacy Badger is turned OFF while using the link')