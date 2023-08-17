import requests
import time
import pandas as pd
import json
from pandas.io.json import json_normalize
from loguru import logger
import database, account

frames = {}
print("Retrieving matches ~10mins")


def match_stats(match_list: list, puuid: str, APIKey: str):
    columns = [
        "assists",
        "bountyLevel",
        "champLevel",
        "championName",
        "consumablesPurchased",
        "damageDealtToBuildings",
        "damageDealtToObjectives",
        "damageDealtToTurrets",
        "damageSelfMitigated",
        "deaths",
        "firstBloodAssist",
        "firstBloodKill",
        "firstTowerAssist",
        "firstTowerKill",
        "gameEndedInSurrender",
        "goldEarned",
        "goldSpent",
        "inhibitorKills",
        "inhibitorTakedowns",
        "inhibitorsLost",
        "item1",
        "item2",
        "item3",
        "item4",
        "item5",
        "item6",
        "killingSprees",
        "kills",
        "largestKillingSpree",
        "largestMultiKill",
        "longestTimeSpentLiving",
        "magicDamageDealt",
        "magicDamageDealtToChampions",
        "magicDamageTaken",
        "nexusKills",
        "nexusTakedowns",
        "perks",
        "physicalDamageDealt",
        "physicalDamageDealtToChampions",
        "physicalDamageTaken",
        "puuid",
        "spell1Casts",
        "spell2Casts",
        "spell3Casts",
        "spell4Casts",
        "summoner1Casts",
        "summoner1Id",
        "summoner2Casts",
        "summoner2Id",
        "summonerLevel",
        "summonerName",
        "teamId",
        "timeCCingOthers",
        "timePlayed",
        "totalDamageDealt",
        "totalDamageDealtToChampions",
        "totalDamageShieldedOnTeammates",
        "totalDamageTaken",
        "totalHeal",
        "totalHealsOnTeammates",
        "totalMinionsKilled",
        "totalTimeSpentDead",
        "trueDamageDealt",
        "trueDamageDealtToChampions",
        "trueDamageTaken",
        "turretKills",
        "turretTakedowns",
        "turretsLost",
        "win",
    ]
    match_list_database = []
    match_list_database = get_list_of_database_matches(puuid)
    print("len matches in database", len(match_list_database))
    for match in match_list:
        exists = check_if_match_saved(match, match_list_database)
        if exists:
            pass
        else:
            URL = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                match, APIKey
            )
            response = requests.get(URL)
            if response.status_code != 200:
                logger.debug(
                    f"For match {match}Error: {response.status_code}: {response.text}"
                )
                break
            json_data = json.loads(response.text)
            teams = json_data["info"]["teams"]
            teams_df = pd.json_normalize(teams)
            teams_df = teams_df.loc[
                :,
                [
                    "teamId",
                    "objectives.champion.first",
                    "objectives.champion.kills",
                    "objectives.inhibitor.first",
                    "objectives.inhibitor.kills",
                    "objectives.tower.first",
                    "objectives.tower.kills",
                ],
            ]
            participants = json_data["info"]["participants"]
            stat_df = pd.DataFrame(participants)
            stat_df = stat_df.loc[:, columns]
            stat_df = pd.merge(
                stat_df, teams_df, how="outer", left_on="teamId", right_on="teamId"
            )
            stat_df["gameDuration"] = round(stat_df["timePlayed"] / 60, 1)
            stat_df["timeStarted"] = json_data["info"]["gameCreation"]
            stat_df["minionDamage"] = (
                stat_df["totalDamageDealt"]
                - stat_df["totalDamageDealtToChampions"]
                - stat_df["damageDealtToBuildings"]
            )
            stat_df = per_min_cols(stat_df)
            stat_df["matchID"] = match
            stat_df["unique_id"] = stat_df["matchID"] + stat_df["puuid"]
            time.sleep(2)
            stat_df = stat_df.drop(columns=["perks"])
            database.write_to_database(stat_df, "Matches", "append")


def per_min_cols(df):
    columns_list = [
        "assists",
        "damageDealtToBuildings",
        "deaths",
        "goldEarned",
        "kills",
        "magicDamageDealt",
        "magicDamageDealtToChampions",
        "magicDamageTaken",
        "minionDamage",
        "physicalDamageDealt",
        "physicalDamageDealtToChampions",
        "physicalDamageTaken",
        "spell1Casts",
        "spell2Casts",
        "spell3Casts",
        "spell4Casts",
        "totalDamageDealt",
        "totalDamageDealtToChampions",
        "totalDamageShieldedOnTeammates",
        "totalDamageTaken",
        "totalHeal",
        "totalHealsOnTeammates",
        "totalMinionsKilled",
        "totalTimeSpentDead",
    ]
    for col in columns_list:
        df[f"{col}_pm"] = round(df.loc[:, col] / df.loc[:, "gameDuration"], 1)
    return df


def check_if_match_saved(match: str, database_match_list: list):
    """Check if a match is in the list"""
    if match in database_match_list:
        return True
    else:
        return False


def get_list_of_database_matches(puuid: str) -> list:
    """Gets a list of all database match ids based on puuid"""
    query = f"Select Distinct(matchID) from Matches where puuid = '{puuid}'"
    df = database.read_database(query)
    return list(df["matchID"].unique())
