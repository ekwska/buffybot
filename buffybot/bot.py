#!/usr/bin/env python
# bot.py
import os
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from buffybot.BuffyBot import BuffyBot

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents(messages=True, message_content=True)

bot = commands.Bot(command_prefix="!", intents=intents)
bot.add_cog(BuffyBot(bot))


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord! Version {discord.__version__}")
    await bot.load_extension("buffybot.BuffyBot")
    logging.info(f"{bot.user} has loaded the BuffyBot extension!")
    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} commands.")
    except Exception as e:
        logging.error(e)


bot.run(TOKEN)
