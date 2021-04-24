#!/usr/bin/env python
# bot.py
import os
import random

from discord import Member
from discord.ext import commands
from dotenv import load_dotenv

from tqdm import tqdm
from time import sleep

from buffybot.SeasonScraper.SeasonScraper import SeasonScraper


class BuffyBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.master_table = SeasonScraper().master_table
    
    @commands.command(name='current_episode', help='Responds with the episode you are currently on')
    async def current_episode(self, ctx):
        brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)
    
    @commands.command(name='current_season', help='Responds with the season you are currently in')
    async def current_seasom(self, ctx):
        brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)
    
    @commands.command(name='next_episode', help='Responds with the episode you want to watch next')
    async def next_episode(self, ctx):
        brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name='progress_season', help='Responds with a progress bar showing how many episodes you have left in the current season')
    async def progress_season(self, ctx):
        season = "1"
        bar_len = 100
        count = 25
        total = 100
        status = ''
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        await ctx.send('[%s] %s%s through season %s%s\r' % (bar, percents, '%', season, status))

    @commands.command(name='save', help='Save your current progress. Saving your progress means that you JUST FINISHED the episode!')
    async def save_progress(self, ctx):
        season = "1"
        bar_len = 100
        count = 25
        total = 100
        status = ''
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        await ctx.send(self.get_episode_summary(1, 1))

    @commands.command(name='progress_buffy', help='Responds with a progress bar showing how many episodes you have left in the Buffy marathon')
    async def progress_buffy(self, ctx):
        bar_len = 100
        count = 25
        total = 100
        status = ''
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        await ctx.send('[%s] %s%s through Buffy the Vampire Slayer %s\r' % (bar, percents, '%', status))

    def get_episode_summary(self, season : int, episode : int):
        return self.master_table[(self.master_table['Season Number'] == season) & (self.master_table['No. inseason'] == episode) ]