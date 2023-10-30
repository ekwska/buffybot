#!/usr/bin/env python
# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from buffybot.BuffyBot import BuffyBot

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents(messages=True, message_content=True)

bot = commands.Bot(command_prefix="!", intents=intents)
bot.add_cog(BuffyBot(bot))


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! Version {discord.__version__}')
    await bot.load_extension("buffybot.BuffyBot")
    print(f"{bot.user} has loaded the BuffyBot extension!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

# try:
#     synced = await bot.tree.sync()
#     print(f"Synced {len(synced)} commands.")
# except Exception as e:
#     print(e)

bot.run(TOKEN)
