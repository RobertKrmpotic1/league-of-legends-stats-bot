import requests
import pandas as pd
import json
from pandas.io.json import json_normalize

match_df = pd.DataFrame()
# just get aram data #aram que = 450
# uses Account ID in order to get recent matches played
# "https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/0M5wvh-e2y7mfwvUdj0JQYN5kYb596s_tQinvYgL_dolLA?queue=450&endIndex=100&beginIndex=0&api_key=RGAPI-83c309f0-873a-4a16-8073-01898b18f42a"
history_lenght = [0, 100, 200, 300, 400]


def get_match_history(puuID, APIKey):
    history_list = []
    for n in history_lenght:
        startIndex = n
        count = 100
        URL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue=450&start={}&count={}&api_key={}".format(
            puuID, startIndex, count, APIKey
        )
        response = requests.get(URL)
        json_data = json.loads(response.text)
        history_list.extend(json_data)
    return history_list
