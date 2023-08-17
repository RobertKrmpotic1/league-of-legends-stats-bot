from datetime import datetime
from loguru import logger
import pandas as pd
import account, match_history, match, database
from config import APIConfig, Time


def update_user_matches(
    puuid: str, APIKey: str, games_amount: int = 200, step: int = 100
) -> bool:
    """Gets a list of matches and updates new ones to the database"""
    match_history_list = match_history.get_match_history(
        puuid, APIKey, games_amount, step
    )
    # update database with matches
    match.match_stats(match_history_list, puuid, APIKey)
    # updates users table with new stats
    df = database.read_database(f"select * from Matches where puuid = '{puuid}'")
    account.add_user_to_users_table(df, puuid)
    return True


def check_winrate(puuid: str, APIKey: str):
    """Checks winrate from the Users table"""
    df = database.read_database(f"select * from Users where puuid = '{puuid}'")
    print(df.head())
    if len(df) > 0:
        winrate = df["win_rate"].values[0]
        gamecount = df["matches"].values[0]
        percentage = "{:.1%}".format(winrate)
        return percentage, gamecount
    else:
        return 0, 0


def check_today_stats(puuid: str):
    """Looks at matches database and checks winrate and games played"""
    df = database.read_database(f"select * from Matches where puuid = '{puuid}'")
    df_today = df.loc[
        pd.to_datetime(df["timeStarted"], unit="ms").dt.date == Time.today
    ]
    games_today = len(df_today)
    games_won = df_today["win"].sum()
    return games_today, games_won


def get_puuid(summonerName: str, APIKey: str):
    """Gets puuid from summonername (EUNE only)"""
    accountID, puuid = account.getaccountID(summonerName, APIKey)
    print(puuid)
    return puuid


def command_to_username(message: str):
    """Takes str command and returns username"""
    command_length = len(message.content.split(" ")[0])
    user = message.content[command_length + 1 :]
    return user


def get_comment_for_todays_performance(games_today: int, games_won: int):
    """Get a custom comment on today's performance"""

    if games_today == 0:
        return "First game of the day according to our data"
    else:
        winrate = games_today / games_won

    if (winrate < 0.4) & (games_today > 10):
        return f"The user has played {games_today} and won only {games_won}. \n I'd suggest to take a break, this game ain't for everyone. 🤡"

    elif games_today > 10:
        return f"The user has played {games_today} and won {games_won}. \n Not bad, but consider going outside and touching grass."

    elif winrate > 0.6:
        return f"The user has played {games_today} and won {games_won}. \n Get that 🍞"

    else:
        return "The user has played {games_today} and won {games_won}."
