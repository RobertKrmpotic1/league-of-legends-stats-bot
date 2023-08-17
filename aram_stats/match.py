import requests
import pandas as pd
import json
from pandas.io.json import json_normalize
from os.path import exists
import time


frames = {}
print("Retrieving matches ~10mins")


def match_stats(match_list, APIKey):
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
    for match in match_list:
        exists = check_if_match_saved(match)
        if exists:
            pass
        else:
            URL = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                match, APIKey
            )
            response = requests.get(URL)
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
            time.sleep(2)
            stat_df.to_csv(f"data/matches/{match}.csv")


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


def check_if_match_saved(match):
    path = f"data/matches/{match}.csv"
    return exists(path)
