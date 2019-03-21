import discord
import subprocess
from config import client

async def batch_exec():
    subprocess.call(['ServiceRestart.bat'], shell=False)