import discord
import aiohttp
from config import client

titles = [
    '@mission-maker',
    '@minecraft',
    '@eco'
]
descriptions = [
    '''
    This role gives access to the mission making channels. Everyone is free to give mission making a try.
    **__Requirements__**
    *> Attend at least 1 Saturday Op*
    *> Understand that we make missions differently than other units*
    ''',
    '''
    Allows other people who play Minecraft to ping your role directly.
    ''',
    '''
    Allows other people who play Eco to ping you about how there isn't a server anymore.
    '''
]
names = [
    'Mission Making',
    'Minecraft',
    'Eco'
]