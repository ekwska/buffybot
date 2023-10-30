#!/usr/bin/env python
# SeasonScraper.py
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
import logging
from buffybot.utils import get_project_root
from discord.utils import setup_logging

setup_logging(level=logging.INFO, root=True)


class SeasonScraper:
    def __init__(self):
        self.season_table_end = 7  # the final season table
        self.main_table_fpath = os.path.join(
            get_project_root(), "data", "season_list.csv"
        )
        self.main_table = self.get_main_table()

    def get_main_table(self):
        if os.path.exists(self.main_table_fpath):
            main_table = self.load_main_table()
        else:
            main_table = self.generate_main_table()
        return main_table

    def load_main_table(self) -> pd.DataFrame:
        logging.info("Main table of seasons/episodes exists, loading!")
        return pd.read_csv(self.main_table_fpath)

    def generate_main_table(self) -> pd.DataFrame:
        logging.info("Main table of seasons/episodes does not exist, generating!")
        url = "https://en.wikipedia.org/wiki/List_of_Buffy_the_Vampire_Slayer_episodes"
        html = urlopen(url)

        # table 1 to table 7 are episode tables
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        dfs = []

        for i, table in enumerate(tables):
            if i == 0:
                continue
            df = pd.read_html(str(table))[0]

            episode_links = self.episode_urls(table)
            df["episode_url"] = episode_links
            dfs.append(df)
            if i == self.season_table_end:
                break
        main_dataframe = pd.concat(dfs, ignore_index=True)
        main_dataframe = self.add_season_numbers_to_main(main_dataframe)

        if not os.path.exists(self.main_table_fpath):
            main_dataframe.to_csv(self.main_table_fpath, index=False)

        return main_dataframe

    def episode_urls(self, table, episode_column=1) -> list:
        episode_urls = []
        for row in table.tbody.findAll("tr"):
            row = row.findAll("td")
            if len(row) != 0:
                # we know that the episode name will always be column 1
                link = row[episode_column].find("a")
                if not link:
                    episode_urls.append("missing")
                else:
                    episode_urls.append("https://en.wikipedia.org" + link["href"])
        return episode_urls

    def add_season_numbers_to_main(self, main_table: pd.DataFrame) -> pd.DataFrame:
        episode_ids_in_season = [[]]
        season_eps = main_table["No. inseason"]
        main_table["Season Number"] = 0

        for current_ep, next_ep in zip(
            season_eps, season_eps[1:]
        ):  # pairwise iteration
            if next_ep - current_ep == 1:
                if not episode_ids_in_season[-1]:
                    episode_ids_in_season[-1].extend((current_ep, next_ep))
                else:
                    episode_ids_in_season[-1].append(next_ep)
            elif episode_ids_in_season[-1]:
                # The difference isn't 1 so add a new empty list in case it ended a sequence
                episode_ids_in_season.append([])

        # In case the list doesn't end with a sequence, remove the trailing empty list.
        if not episode_ids_in_season[-1]:
            del episode_ids_in_season[-1]

        # Now copy the unique season values back into the main table
        season_number = 1
        n_prev_eps = 0
        for season_vals in episode_ids_in_season:
            n_current_eps = len(season_vals)
            if n_prev_eps == 0:
                main_table.loc[0:n_current_eps, "Season Number"] = season_number
            else:
                main_table.loc[
                    n_prev_eps : n_prev_eps + n_current_eps, "Season Number"
                ] = season_number
            n_prev_eps = n_prev_eps + n_current_eps
            season_number += 1

        return main_table


if __name__ == "__main__":
    test = SeasonScraper()
    logging.info(test.main_table)
