import requests
import pandas as pd
import json
import database
from datetime import datetime
from config import Time

# find account id
def getaccountID(summonerName, APIKey):
    URL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(
        summonerName, APIKey
    )
    basic_response = requests.get(URL)
    if basic_response.status_code != 200:
        if basic_response.status_code == 404:
            return "", ""

    else:
        json_data = json.loads(basic_response.text)
        basic_df = pd.DataFrame.from_dict(json_data, orient="index")
        basic_df = basic_df.transpose()
        basic_df.index = basic_df["name"]
        return basic_df["accountId"][0], basic_df["puuid"][0]


def insert_user(df, puuid):
    """Inserts new row into table"""
    user_dict = calculate_user_stats(df, puuid)
    query = f"""
        INSERT INTO Users 
        ('puuid', 
        'summoner_name', 
        'win_rate', 
        'matches',
       'last_updated_game_datetime', 
       'last_update_game', 
       'etl_timestamp')

        VALUES 
        (
        '{user_dict['puuid']}', 
        '{user_dict['summoner_name']}', 
        {user_dict['win_rate']}, 
        {user_dict['matches']},
       '{user_dict['last_updated_game_datetime']}', 
       '{user_dict['last_update_game']}', 
       '{user_dict['etl_timestamp']}'
       )
    """
    database.execute_query(query)


def update_user(df, puuid):
    """Updates existing row"""
    user_dict = calculate_user_stats(df, puuid)
    query = f"""
    UPDATE 
    Users
    SET 
    summoner_name = '{user_dict['summoner_name']}',
    win_rate = {user_dict['win_rate']},
    matches = {user_dict['matches']},
    last_updated_game_datetime = '{user_dict['last_updated_game_datetime']}',
    last_update_game = '{user_dict['last_update_game']}',
    etl_timestamp = '{user_dict['etl_timestamp']}'
    WHERE puuid = '{user_dict['puuid']}'
    """
    database.execute_query(query)


def calculate_user_stats(df: pd.DataFrame, puuid: str) -> dict:
    user_dict = {}
    user_dict["puuid"] = puuid
    df_temp = df.loc[df["puuid"] == puuid].reset_index()
    user_dict["summoner_name"] = df_temp.loc[0, "summonerName"]
    user_dict["win_rate"] = round(df_temp["win"].mean(), 5)
    user_dict["matches"] = len(df_temp)
    last_game_time = df_temp["timeStarted"].max()
    user_dict["last_updated_game_datetime"] = pd.Timestamp(
        last_game_time, unit="ms"
    ).strftime("%d/%m/%Y %H:%M:%S")
    user_dict["last_update_game"] = df_temp.loc[
        df_temp["timeStarted"] == last_game_time
    ]["matchID"].values[0]
    user_dict["etl_timestamp"] = Time.now.strftime("%d/%m/%Y %H:%M:%S")
    return user_dict


def add_user_to_users_table(df: pd.DataFrame, puuid: str):
    """Insert or update Users table"""
    # check if user in Users table
    query = f""" Select matches from Users where puuid = '{puuid}' """
    if len(database.read_database(query)) == 0:
        print("inserting user")
        insert_user(df, puuid)
    else:
        print("updating user")
        update_user(df, puuid)
