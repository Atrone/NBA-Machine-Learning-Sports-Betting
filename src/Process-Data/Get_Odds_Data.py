import random
import time
import pandas as pd
import sqlite3
import os
import sys

from datetime import datetime, timedelta, date
from tqdm import tqdm
from sbrscrape import Scoreboard
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Utils.tools import get_date
from Utils.Variables import year, season, parent_dir
parent_dir = '\\'.join(str(parent_dir).split('\\')[:-2])
month = [10, 11, 12, 1, 2, 3, 4, 5, 6]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

begin_year_pointer = year[0]
end_year_pointer = year[0]
count = 0

sportsbook='bet365'
df_data = []


con = sqlite3.connect(rf"{parent_dir}\NBA-Machine-Learning-Sports-Betting\Data\odds.sqlite")

for season1 in tqdm(season):
    teams_last_played = {}
    for month1 in tqdm(month):
        if month1 == 1:
            count += 1
            end_year_pointer = year[count]
        for day1 in tqdm(days):
            if month1 == 10 and day1 < 24:
                continue
            if month1 in [4, 6, 9, 11] and day1 > 30:
                continue
            if month1 == 2 and day1 > 28:
                continue
            # skip future games
            if datetime.now() < datetime(year=int(end_year_pointer), month=month1, day=day1):
                continue
            print(f"{end_year_pointer}-{month1:02}-{day1:02}")
            sb = Scoreboard(date=f"{end_year_pointer}-{month1:02}-{day1:02}")
            if not hasattr(sb, "games"):
                continue
            for game in sb.games:
                if game['home_team'] not in teams_last_played:
                    teams_last_played[game['home_team']] = get_date(f"{season1}-{month1:02}{day1:02}")
                    home_games_rested = timedelta(days=7)  # start of season, big number
                else:
                    current_date = get_date(f"{season1}-{month1:02}{day1:02}")
                    home_games_rested = current_date - teams_last_played[game['home_team']]
                    teams_last_played[game['home_team']] = current_date
                    # todo update row

                if game['away_team'] not in teams_last_played:
                    teams_last_played[game['away_team']] = get_date(f"{season1}-{month1:02}{day1:02}")
                    away_games_rested = timedelta(days=7)  # start of season, big number
                else:
                    current_date = get_date(f"{season1}-{month1:02}{day1:02}")
                    away_games_rested = current_date - teams_last_played[game['away_team']]
                    teams_last_played[game['away_team']] = current_date

                try:
                    df_data.append({
                        'Unnamed: 0': 0,
                        'Date': f"{season1}-{month1:02}{day1:02}",
                        'Home': game['home_team'],
                        'Away': game['away_team'],
                        'OU': game['total'][sportsbook],
                        'Spread': game['away_spread'][sportsbook],
                        'ML_Home': game['home_ml'][sportsbook],
                        'ML_Away': game['away_ml'][sportsbook],
                        'Points': game['away_score'] + game['home_score'],
                        'Win_Margin': game['home_score'] - game['away_score'],
                        'Days_Rest_Home': home_games_rested.days,
                        'Days_Rest_Away': away_games_rested.days
                    })
                except KeyError:
                    print(f"No {sportsbook} odds data found for game: {game}")
            time.sleep(random.randint(1, 3))
    begin_year_pointer = year[count]

    df = pd.DataFrame(df_data, )
    df.to_sql(f"odds_{season1}", con, if_exists="replace")
con.close()