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
    print(f"{bot.user} is running..")
    await bot.load_extension("buffybot.BuffyBot")
    print("file loaded")


bot.run(TOKEN)
