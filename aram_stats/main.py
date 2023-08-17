import requests
import json
import os
import time
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import champions, account, match_history, match, aggregate, leaderboard

APIKey = "RGAPI-0fc93db5-5274-4965-a774-d8e1a3178a49"
region = "eun1"
summonerName = "Highly Religious"
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 500)
pd.options.display.float_format = "{:,.2f}".format

print("starting..")


def main(summonerName, APIKey):
    print(f"starting loop for {summonerName}")
    accountID, puuID = account.getaccountID(summonerName, APIKey)
    print("getting match list")
    match_history_list = match_history.get_match_history(puuID, APIKey)

    # get the data
    print("getting match details")
    match.match_stats(match_history_list, APIKey)

    # aggregate
    print("aggregating")
    df_dict = aggregate.create_dict_of_dfs(match_history_list, puuID)
    champ_stats = aggregate.get_champ_stats(df_dict)
    champ_stats.to_excel(f"data/accounts/{summonerName}_champ_stats.xlsx")
    print("saving champ stats")

    account_stats = aggregate.get_account_stats(df_dict, summonerName)

    # add to leaderboard
    leaderboard.add_acc_to_leaderboard(account_stats)
    print("data saved in accounts folder")


summonerlist = [
    "Lectric",
    "HeziK",
    "Call me Rose",
    "Highly Religious",
    "Mafla Jinx",
    "Junachina",
    "Marlov7",
    "Hobo",
    "hypixel skywars",
    "Magnifiko666",
    "Battleborn Kayle",
]
for summoner in summonerlist:
    print(summoner)
    main(summoner, APIKey)
print("done done done!")
