import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.Utils.Expected_Value import expected_value


def _season_from_date_str(date_str: str) -> str:
    """Return season string like '2018-19' from YYYY-MM-DD date string.

    Args:
        date_str: Date string in format YYYY-MM-DD

    Returns:
        Season string 'YYYY-YY'.
    """
    # derive season by NBA convention (season year starts in Oct)
    year, month, _ = [int(x) for x in date_str.split('-')]
    start_year = year if month >= 8 else year - 1
    end_year_two = (start_year + 1) % 100
    return f"{start_year}-{end_year_two:02d}"


def _load_dataset(dataset_path: str, table: str) -> pd.DataFrame:
    """Load full dataset table from sqlite.

    Args:
        dataset_path: Absolute path to dataset.sqlite
        table: Table name inside sqlite

    Returns:
        DataFrame of dataset.
    """
    # open sqlite connection to the dataset file
    con = sqlite3.connect(dataset_path)
    try:
        df = pd.read_sql_query(f"select * from \"{table}\"", con, index_col="index")
    finally:
        con.close()
    return df


def _load_odds_for_season(odds_path: str, season: str) -> pd.DataFrame:
    """Load odds table for a given season from OddsData.sqlite.

    Args:
        odds_path: Absolute path to OddsData.sqlite
        season: Season string 'YYYY-YY'

    Returns:
        DataFrame of odds for the season.
    """
    con = sqlite3.connect(odds_path)
    try:
        # attempt to read the preferred *_new table first
        preferred = f"odds_{season}_new"
        # inline comment: check sqlite master for table existence
        exists = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", con)
        names = set(exists['name'].tolist())
        table_name = preferred if preferred in names else f"odds_{season}"
        if table_name not in names:
            # inline comment: no odds table available for this season
            return pd.DataFrame()
        df = pd.read_sql_query(f"select * from \"{table_name}\"", con, index_col="index")
    finally:
        con.close()
    return df


def _prepare_features_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """Split dataset into features and targets for ML moneyline task.

    Args:
        df: Full dataset frame including label/metadata columns

    Returns:
        (X, y, meta) where X are features, y is Home-Team-Win label, meta includes TEAM_NAME, Date, TEAM_NAME.1, Date.1
    """
    # select columns to exclude that are labels or metadata
    meta_cols = ['TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU']
    y = df['Home-Team-Win']
    drop_cols = ['Score', 'Home-Team-Win', 'OU-Cover'] + meta_cols
    X = df.drop(columns=drop_cols, errors='ignore')
    meta = df[['TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1']].copy()
    return X, y, meta


def _build_odds_lookup(odds_df: pd.DataFrame) -> Dict[str, Dict[str, int]]:
    """Build a nested dict lookup for moneyline odds keyed by date and team.

    Args:
        odds_df: Season odds DataFrame with columns including 'Date', 'Home', 'Away', 'ML_Home', 'ML_Away'

    Returns:
        {date_str: {team_name: moneyline_int, team_name: moneyline_int}}
    """
    # create mapping: date -> {team -> moneyline}
    lookup: Dict[str, Dict[str, int]] = {}
    for row in odds_df.itertuples(index=False):
        # Expected columns order from Get_Odds_Data writer
        date_str = str(getattr(row, 'Date'))
        home = getattr(row, 'Home')
        away = getattr(row, 'Away')
        ml_home = getattr(row, 'ML_Home', None)
        ml_away = getattr(row, 'ML_Away', None)
        if date_str not in lookup:
            lookup[date_str] = {}
        if ml_home is not None:
            lookup[date_str][home] = int(ml_home)
        if ml_away is not None:
            lookup[date_str][away] = int(ml_away)
    return lookup


def _append_result(results_by_date: Dict[str, Dict[str, Dict]], date_str: str, home: str, away: str,
                   ev_home: float, ev_away: float,
                   outcome_home: int, outcome_away: int,
                   ml_home: int, ml_away: int) -> None:
    """Append a single game result into the per-date result mapping.

    Args:
        results_by_date: Mapping of date -> team -> metrics
        date_str: Game date string
        home: Home team name
        away: Away team name
        ev_home: Expected value for home team
        ev_away: Expected value for away team
        outcome_home: 1 if home won, else 0
        outcome_away: 1 if away won, else 0
        ml_home: Moneyline for home team
        ml_away: Moneyline for away team
    """
    # ensure date entry exists
    if date_str not in results_by_date:
        results_by_date[date_str] = {}
    # insert metrics for each team
    results_by_date[date_str][home] = {"EV": float(ev_home), "OUTCOME": int(outcome_home), "ML": int(ml_home) if ml_home is not None else None}
    results_by_date[date_str][away] = {"EV": float(ev_away), "OUTCOME": int(outcome_away), "ML": int(ml_away) if ml_away is not None else None}


def run_backtest(
    dataset_sqlite_path: str = os.path.abspath(os.path.join(os.getcwd(), 'Data', 'dataset.sqlite')),
    odds_sqlite_path: str = os.path.abspath(os.path.join(os.getcwd(), 'Data', 'OddsData.sqlite')),
    dataset_table: str = 'dataset_2012-24_new',
    start_year: int = 2018,
    end_year: int = 2024,
    output_json_path: str = os.path.abspath(os.path.join(os.getcwd(), 'Data', 'backtest_ev_2018_2024.json')),
    max_dates: int | None = None
) -> str:
    """Run walk-forward backtest 2018-2024.

    Trains on all games strictly prior to each holdout date. Predicts the holdout game's
    home win probability using Logistic Regression, computes EVs using moneyline odds from
    seasonal odds tables, and writes results in the required nested JSON format.

    Returns the output file path.
    """
    # load full dataset
    df = _load_dataset(dataset_sqlite_path, dataset_table)
    # ensure Date fields are strings
    df['Date'] = df['Date'].astype(str)
    df['Date.1'] = df['Date.1'].astype(str)

    # sort by chronological order using home team date
    df_sorted = df.sort_values(by=['Date'])

    X_all, y_all, meta_all = _prepare_features_targets(df_sorted)

    # accumulate results in a per-date mapping to aggregate multiple games per date
    results_by_date: Dict[str, Dict[str, Dict]] = {}

    # walk-forward by unique dates in range
    unique_dates = sorted(df_sorted['Date'].unique())
    # pre-load odds for all seasons in range to avoid repeated I/O
    seasons = sorted({ _season_from_date_str(d) for d in unique_dates })
    season_to_odds_lookup: Dict[str, Dict[str, Dict[str, int]]] = {}
    for season in seasons:
        # only load seasons overlapping the requested years
        start = int(season.split('-')[0])
        if start < start_year - 1 or start > end_year:
            continue
        odds_df = _load_odds_for_season(odds_sqlite_path, season)
        season_to_odds_lookup[season] = _build_odds_lookup(odds_df)

    # model we will re-fit as we advance (logistic regression)
    # line comment: keep iterations modest for quick test runs
    model = LogisticRegression(max_iter=200)

    # walk through dates; for each date, train on strictly earlier games, hold out games that occur on this date
    processed_dates = 0  # line comment: track how many dates we've evaluated
    for current_date in unique_dates:
        # filter date range restriction
        year = int(current_date.split('-')[0])
        if year < start_year or year > end_year:
            continue

        # define train mask: all rows whose earliest game date < current_date
        train_mask = df_sorted['Date'] < current_date
        holdout_mask = df_sorted['Date'] == current_date

        if not train_mask.any() or not holdout_mask.any():
            continue

        X_train = X_all[train_mask]
        y_train = y_all[train_mask]
        X_holdout = X_all[holdout_mask]

        # Fit model on training slice
        model.fit(X_train.values.astype(float), y_train.values)

        # Predict probabilities for holdout games
        probs = model.predict_proba(X_holdout.values.astype(float))

        # Extract metadata for holdout to compute EV and outcomes
        meta_holdout = meta_all[holdout_mask]
        y_holdout = y_all[holdout_mask]

        # prepare odds lookup for this date via its season
        season = _season_from_date_str(current_date)
        odds_lookup = season_to_odds_lookup.get(season, {})
        teams_odds_for_date = odds_lookup.get(current_date, {})

        # Iterate row-wise; rows are pairwise home/away features packed into one row already
        # meta has TEAM_NAME (home), TEAM_NAME.1 (away)
        for i, (_, meta_row) in enumerate(meta_holdout.iterrows()):
            home_team = meta_row['TEAM_NAME']
            away_team = meta_row['TEAM_NAME.1']
            # y=1 means home win
            outcome_home = int(y_holdout.iloc[i])
            outcome_away = int(1 - outcome_home)

            # probability array is [P(away), P(home)]
            p_home = float(probs[i][1])
            p_away = float(probs[i][0])

            # fetch moneylines
            ml_home = teams_odds_for_date.get(home_team)
            ml_away = teams_odds_for_date.get(away_team)

            # compute EVs (if odds missing, expected_value will error; guard it)
            ev_home = expected_value(p_home, int(ml_home)) if ml_home is not None else 0.0
            ev_away = expected_value(p_away, int(ml_away)) if ml_away is not None else 0.0

            _append_result(results_by_date, current_date, home_team, away_team,
                           ev_home, ev_away, outcome_home, outcome_away,
                           ml_home if ml_home is not None else 0,
                           ml_away if ml_away is not None else 0)

        # line comment: respect quick-run limit if provided
        processed_dates += 1
        if max_dates is not None and processed_dates >= max_dates:
            break

    # convert mapping to desired list-of-objects format: [{date: {team: {...}}}, ...]
    results: List[Dict] = [{date: teams} for date, teams in sorted(results_by_date.items())]

    # write out JSON
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)

    return output_json_path


if __name__ == '__main__':
    # simple CLI entrypoint
    path = run_backtest()
    print(f"Backtest results written to: {path}")

