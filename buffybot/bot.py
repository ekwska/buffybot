#!/usr/bin/env python
# bot.py
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

from buffybot.BuffyBot import BuffyBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.add_cog(BuffyBot(bot))
bot.run(TOKEN)

