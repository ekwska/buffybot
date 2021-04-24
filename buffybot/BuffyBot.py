#!/usr/bin/env python
# bot.py
import os
import random

from discord import Member, Embed
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

    @commands.command(
        name="current_episode",
        help="Responds with the episode you are currently on",
    )
    async def current_episode(self, ctx):
        current_ep = {
            "season": 2,
            "episode": 5,
        }  # so returns season 1 episode 2
        ep_summary = self.get_episode_summary(
            current_ep["season"], current_ep["episode"]
        )

        embed = Embed(
            title=f"You're watching, season {ep_summary['Season Number'].iloc[0]}, episode {ep_summary['No. inseason'].iloc[0]}",
            url=ep_summary["episode_url"].iloc[0],
            description=f"You are currently watching '{ep_summary['Title'].iloc[0]}'...🦇",
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="next_episode",
        help="Responds with the episode you want to watch next",
    )
    async def next_episode(self, ctx):
        last_ep_watched = {
            "season": 2,
            "episode": 5,
        }  # so returns season 1 episode 2
        ep_summary = self.get_episode_summary(
            last_ep_watched["season"], last_ep_watched["episode"] + 1
        )
        embed = Embed(
            title=f"None",
            description=f"None",
        )
        if ep_summary.empty:

            # A new season is starting!
            ep_summary = self.get_episode_summary(
                last_ep_watched["season"] + 1, 1
            )

            if ep_summary.empty:
                # You finished buffy!
                embed = Embed(
                    title=f"🎉 You finished Buffy! Congratulations! 🎉",
                    description=f"Start again...? 🦇",
                )

        embed = Embed(
            title=f"Next up, season {ep_summary['Season Number'].iloc[0]}, episode {ep_summary['No. inseason'].iloc[0]}",
            url=ep_summary["episode_url"].iloc[0],
            description=f"Next you're watching '{ep_summary['Title'].iloc[0]}'...🦇",
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="progress_season",
        help="Responds with a progress bar showing how many episodes you have left in the current season",
    )
    async def progress_season(self, ctx):
        season = "1"
        bar_len = 100
        count = 25
        total = 100
        status = ""
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "=" * filled_len + "-" * (bar_len - filled_len)

        await ctx.send(
            "[%s] %s%s through season %s%s\r"
            % (bar, percents, "%", season, status)
        )

    @commands.command(
        name="save",
        help="Save your current progress. Saving your progress means that you JUST FINISHED the episode!",
    )
    async def save_progress(self, ctx):
        season = "1"
        bar_len = 100
        count = 25
        total = 100
        status = ""
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "=" * filled_len + "-" * (bar_len - filled_len)

        await ctx.send(self.get_episode_summary(1, 1))

    @commands.command(
        name="progress_buffy",
        help="Responds with a progress bar showing how many episodes you have left in the Buffy marathon",
    )
    async def progress_buffy(self, ctx):
        bar_len = 100
        count = 25
        total = 100
        status = ""
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "=" * filled_len + "-" * (bar_len - filled_len)

        await ctx.send(
            "[%s] %s%s through Buffy the Vampire Slayer %s\r"
            % (bar, percents, "%", status)
        )

    def get_episode_summary(self, season: int, episode: int):
        return self.master_table[
            (self.master_table["Season Number"] == season)
            & (self.master_table["No. inseason"] == episode)
        ]
