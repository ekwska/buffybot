#!/usr/bin/env python
# BuffyBot.py
import os

from discord import Embed
from discord.ext import commands

import json
import logging

from buffybot.SeasonScraper.SeasonScraper import SeasonScraper
from buffybot.utils import get_project_root

logging.basicConfig(level=logging.INFO)


async def setup(bot):
    print("inside setup function")
    await bot.add_cog(BuffyBot(bot))


class BuffyBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.master_table = SeasonScraper().master_table
        self.total_eps = self.master_table.iloc[-1]["No.overall"]
        self.current_ep = {}
        self.current_progress_fpath = os.path.join(
            get_project_root(), "data", "progress.json"
        )

    @commands.hybrid_command(
        name="current",
        help="Responds with the episode you are currently on",
    )
    async def current_episode(self, ctx):
        logging.info("current episode")
        self.update_current_ep()

        if not self.current_ep:
            embed = self.no_progress_embed()
        else:
            ep_summary = self.get_episode_summary(
                self.current_ep["season"], self.current_ep["episode"]
            )

            embed = Embed(
                title=f"You're watching, season {ep_summary['Season Number'].iloc[0]}, episode {ep_summary['No. inseason'].iloc[0]}",
                url=ep_summary["episode_url"].iloc[0],
                description=f"You are currently watching {ep_summary['Title'].iloc[0]}...🦇",
            )

        await ctx.send(embed=embed)

    @commands.command(
        name="next",
        help="Responds with the episode you want to watch next",
    )
    async def next_episode(self, ctx):
        logging.info("next episode")
        if not self.current_ep:
            self.update_current_ep()
            if not self.current_ep:  # if still empty, we don't know where we are
                embed = self.no_progress_embed()
                await ctx.send(embed=embed)

        ep_summary = self.get_episode_summary(
            self.current_ep["season"], self.current_ep["episode"] + 1
        )
        embed = Embed(
            title=f"None",
            description=f"None",
        )
        if ep_summary.empty:
            # A new season is starting!
            ep_summary = self.get_episode_summary(self.current_ep["season"] + 1, 1)

            if ep_summary.empty:
                # You finished buffy!
                embed = Embed(
                    title=f"🎉 You finished Buffy! Congratulations! 🎉",
                    description=f"Start again...? 🦇",
                )

        embed = Embed(
            title=f"Next up, season {ep_summary['Season Number'].iloc[0]}, episode {ep_summary['No. inseason'].iloc[0]}",
            url=ep_summary["episode_url"].iloc[0],
            description=f"Next you're watching {ep_summary['Title'].iloc[0]}...🦇",
        )

        await ctx.send(embed=embed)

    @commands.command(
        name="save",
        help="Save your current progress. Saving your progress means that you will be JUST STARTING the episode next time!",
    )
    async def save_progress(self, ctx, season: int, episode: int):
        logging.info("save episode")
        ep_summary = self.get_episode_summary(season, episode)

        ep_json = {"season": season, "episode": episode}
        with open(self.current_progress_fpath, "w") as f:
            json.dump(ep_json, f)

        embed = Embed(
            title=f"You are watching season {ep_summary['Season Number'].iloc[0]}, episode {ep_summary['No. inseason'].iloc[0]}",
            url=ep_summary["episode_url"].iloc[0],
            description=f"You're watching {ep_summary['Title'].iloc[0]}...🦇",
        )
        self.current_ep = {"season": season, "episode": episode}
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="progress",
        help="Responds with a progress bar showing how many episodes you have left in the Buffy marathon",
    )
    async def progress(self, ctx):
        logging.info("progress")
        if not self.current_ep:
            self.update_current_ep()
            if not self.current_ep:  # if still empty, we don't know where we are
                embed = self.no_progress_embed()
                await ctx.send(embed=embed)

        ep_summary = self.get_episode_summary(
            self.current_ep["season"], self.current_ep["episode"]
        )

        bar_len = 100
        count = ep_summary["No.overall"].iloc[0]
        total = self.total_eps
        status = ""
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "=" * filled_len + "-" * (bar_len - filled_len)

        await ctx.send(
            "[%s] %s%s through Buffy the Vampire Slayer %s\r"
            % (bar, percents, "%", status)
        )

    def get_episode_summary(self, season: int, episode: int):
        logging.info("episode summary")
        return self.master_table[
            (self.master_table["Season Number"] == season)
            & (self.master_table["No. inseason"] == episode)
        ]

    def update_current_ep(self):
        try:
            f = open(self.current_progress_fpath)
            self.current_ep = json.load(f)
        except FileNotFoundError:
            self.current_ep = {}

    def no_progress_embed(self):
        return Embed(
            title=f"I don't know where you're up to...💀",
            description=f"Use the command '!save season episode' to record your progess so far",
        )
