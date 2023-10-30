#!/usr/bin/env python
# SeasonScraper.py
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
from buffybot.utils import get_project_root


class SeasonScraper:
    def __init__(self):
        self.season_table_end = 7  # the final season table
        self.master_table_fpath = os.path.join(
            get_project_root(), "data", "season_list.csv"
        )
        self.master_table = self.get_master_table()

    def get_master_table(self):
        if os.path.exists(self.master_table_fpath):
            master_table = self.load_master_table()
        else:
            master_table = self.generate_master_table()
        return master_table

    def load_master_table(self) -> pd.DataFrame:
        print("Master table exists, loading!")
        return pd.read_csv(self.master_table_fpath)

    def generate_master_table(self) -> pd.DataFrame:
        print("Master table does not exist, generating!")
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
        master_dataframe = pd.concat(dfs, ignore_index=True)
        master_dataframe = self.add_season_numbers_to_master(master_dataframe)

        if not os.path.exists(self.master_table_fpath):
            master_dataframe.to_csv(self.master_table_fpath, index=False)

        return master_dataframe

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

    def add_season_numbers_to_master(self, master_table: pd.DataFrame) -> pd.DataFrame:
        episode_ids_in_season = [[]]
        season_eps = master_table["No. inseason"]
        master_table["Season Number"] = 0

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

        # Now copy the unique season values back into the master table
        season_number = 1
        n_prev_eps = 0
        for season_vals in episode_ids_in_season:
            n_current_eps = len(season_vals)
            if n_prev_eps == 0:
                master_table.loc[0:n_current_eps, "Season Number"] = season_number
            else:
                master_table.loc[
                    n_prev_eps : n_prev_eps + n_current_eps, "Season Number"
                ] = season_number
            n_prev_eps = n_prev_eps + n_current_eps
            season_number += 1

        return master_table


if __name__ == "__main__":
    test = SeasonScraper()
    print(test.master_table)
