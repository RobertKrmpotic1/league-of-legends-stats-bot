import pandas as pd
from os.path import exists


def add_acc_to_leaderboard(df):
    if leaderboard_file_exists():
        df_leader = pd.read_csv("data/accounts/leaderboard.csv", index_col="Name")
        if df["puuid"][0] in df_leader["puuid"].values:
            df_leader.loc[df_leader["puuid"] == df["puuid"][0]] = df
        else:
            df_leader = pd.concat([df_leader, df], axis=0)
        df_leader = df_leader.sort_values(by="Win Rate", ascending=False)
        df_leader.reset_index(inplace=True)
        df_leader = df_leader.loc[
            :,
            [
                "Name",
                "Win Rate",
                "Games played",
                "Games won",
                "Avg game time",
                "Team first tower %",
                "Team first inhib %",
                "Avg damage to champs",
                "Avg healing on others",
                "Avg shielding on others",
                "Avg Damage taken",
                "Avg damage to towers",
                "puuid",
            ],
        ]
        df_leader.to_csv("data/accounts/leaderboard.csv")
        print("added to leaderboard")
    else:
        df.to_csv("data/accounts/leaderboard.csv")
        print("made leaderboard file")


def leaderboard_file_exists():
    path = f"data/accounts/leaderboard.csv"
    return exists(path)
