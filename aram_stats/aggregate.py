import pandas as pd
import numpy as np


def create_dict_of_dfs(match_list, puuID):
    df_dict = {}
    for match in match_list:
        df = pd.read_csv(f"data/matches/{match}.csv")
        df_dict[match] = df.loc[df["puuid"] == puuID]
    return df_dict


def get_champ_stats(df_dict):
    df_champs = pd.concat(df_dict, axis=0)
    print(len(df_champs))
    df_agg = pd.DataFrame()
    # games
    df_agg["Games played"] = df_champs["championName"].value_counts()
    df_agg["Games won"] = df_champs.groupby("championName")["win"].sum().astype(int)
    df_agg["Win rate"] = round(
        ((df_agg["Games won"] / df_agg["Games played"]) * 100), 1
    )
    df_agg["Game time"] = round(
        (df_champs.groupby("championName").agg({"gameDuration": np.average})), 1
    )

    # damage to champs
    df_agg["Damage to champs"] = round(
        df_champs.groupby("championName").agg(
            {"totalDamageDealtToChampions": np.average}
        ),
        0,
    )
    df_agg["PM Damage to champs"] = round(
        df_champs.groupby("championName").agg(
            {"totalDamageDealtToChampions_pm": np.average}
        ),
        0,
    )
    df_agg["Damage taken"] = round(
        df_champs.groupby("championName").agg({"totalDamageTaken": np.average}), 0
    )
    df_agg["PM Damage taken"] = round(
        df_champs.groupby("championName").agg({"totalDamageTaken_pm": np.average}), 0
    )

    # towers
    df_agg["Damage to towers"] = round(
        df_champs.groupby("championName").agg({"damageDealtToBuildings": np.average}), 0
    )
    df_agg["PM Damage to towers"] = round(
        df_champs.groupby("championName").agg(
            {"damageDealtToBuildings_pm": np.average}
        ),
        0,
    )
    df_agg["Turret takedowns"] = round(
        df_champs.groupby("championName").agg({"turretTakedowns": np.average}), 1
    )
    df_agg["Inhibitor takedowns"] = round(
        df_champs.groupby("championName").agg({"inhibitorTakedowns": np.average}), 1
    )

    df_agg["Team first tower %"] = round(
        (
            df_champs.groupby("championName")["objectives.tower.first"]
            .sum()
            .astype(int)
            / df_agg["Games played"]
        )
        * 100,
        1,
    )
    df_agg["Team first inhib %"] = round(
        (
            df_champs.groupby("championName")["objectives.inhibitor.first"]
            .sum()
            .astype(int)
            / df_agg["Games played"]
        )
        * 100,
        1,
    )

    # minions
    df_agg["Damage to minions"] = round(
        df_champs.groupby("championName").agg({"minionDamage": np.average}), 0
    )
    df_agg["PM Damage to minions"] = round(
        df_champs.groupby("championName").agg({"minionDamage_pm": np.average}), 0
    )
    df_agg["Minions slain"] = round(
        df_champs.groupby("championName").agg({"totalMinionsKilled": np.average}), 0
    )
    df_agg["PM Minions slain"] = round(
        df_champs.groupby("championName").agg({"totalMinionsKilled_pm": np.average}), 1
    )

    # supporting
    df_agg["Ally healing"] = round(
        df_champs.groupby("championName").agg({"totalHealsOnTeammates": np.average}), 0
    )
    df_agg["PM Ally healing"] = round(
        df_champs.groupby("championName").agg({"totalHealsOnTeammates_pm": np.average}),
        1,
    )
    df_agg["Ally shielding"] = round(
        df_champs.groupby("championName").agg(
            {"totalDamageShieldedOnTeammates": np.average}
        ),
        0,
    )
    df_agg["PM Ally shielding"] = round(
        df_champs.groupby("championName").agg(
            {"totalDamageShieldedOnTeammates_pm": np.average}
        ),
        1,
    )

    # KDA
    df_agg["Kills"] = round(
        df_champs.groupby("championName").agg({"kills": np.average}), 1
    )
    df_agg["PM Kills"] = round(
        df_champs.groupby("championName").agg({"kills_pm": np.average}), 1
    )
    df_agg["Deaths"] = round(
        df_champs.groupby("championName").agg({"deaths": np.average}), 1
    )
    df_agg["PM Deaths"] = round(
        df_champs.groupby("championName").agg({"deaths_pm": np.average}), 1
    )
    df_agg["Assists"] = round(
        df_champs.groupby("championName").agg({"assists": np.average}), 1
    )
    df_agg["PM Assists"] = round(
        df_champs.groupby("championName").agg({"assists_pm": np.average}), 1
    )

    # gold and economy
    df_agg["Gold Earned"] = round(
        df_champs.groupby("championName").agg({"goldEarned": np.average}), 0
    )
    df_agg["PM Gold Earned"] = round(
        df_champs.groupby("championName").agg({"goldEarned_pm": np.average}), 1
    )
    df_agg["Passive gold %"] = round(
        ((df_agg["Game time"] - 1) * 330 / df_agg["Gold Earned"]) * 100, 1
    )
    df_agg["Gold Spent"] = round(
        df_champs.groupby("championName").agg({"goldSpent": np.average}), 0
    )

    # spell casting
    df_agg["PM Q cast"] = round(
        df_champs.groupby("championName").agg({"spell1Casts_pm": np.average}), 1
    )
    df_agg["PM W cast"] = round(
        df_champs.groupby("championName").agg({"spell2Casts_pm": np.average}), 1
    )
    df_agg["PM E cast"] = round(
        df_champs.groupby("championName").agg({"spell3Casts_pm": np.average}), 1
    )
    df_agg["PM R cast"] = round(
        df_champs.groupby("championName").agg({"spell4Casts_pm": np.average}), 1
    )

    return df_agg


def get_account_stats(df_dict, summonerName):
    df = pd.concat(df_dict, axis=0)
    df_agg = pd.DataFrame()
    df_agg.at[f"{summonerName}", "Name"] = summonerName
    df_agg = df_agg.set_index("Name")
    df_agg["Games played"] = len(df)
    df_agg["Games won"] = df["win"].sum()
    df_agg["Win Rate"] = round(
        ((df_agg["Games won"] / df_agg["Games played"]) * 100), 1
    )
    df_agg["Avg game time"] = round(df["gameDuration"].mean(), 1)
    df_agg["Team first tower %"] = (
        round(df["objectives.tower.first"].astype(int).mean(), 3) * 100
    )
    df_agg["Team first inhib %"] = (
        round(df["objectives.inhibitor.first"].astype(int).mean(), 3) * 100
    )
    df_agg["Avg damage to champs"] = round(df["totalDamageDealtToChampions"].mean(), 0)
    df_agg["Avg damage to towers"] = round(df["damageDealtToBuildings"].mean(), 0)
    df_agg["Avg shielding on others"] = round(
        df["totalDamageShieldedOnTeammates"].mean(), 0
    )
    df_agg["Avg healing on others"] = round(df["totalHealsOnTeammates"].mean(), 0)
    df_agg["Avg Damage taken"] = round(df["totalDamageTaken"].mean(), 0)

    df_agg["puuid"] = df.loc[:, "puuid"][0]

    return df_agg
