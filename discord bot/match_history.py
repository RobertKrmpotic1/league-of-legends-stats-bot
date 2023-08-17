from asyncio.log import logger
import requests
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

match_df = pd.DataFrame()
# uses Account ID in order to get recent matches played
# "https://eun1.api.riotgames.com/lol/match/v4/matchlists/by-account/0M5wvh-e2y7mfwvUdj0JQYN5kYb596s_tQinvYgL_dolLA?queue=450&endIndex=100&beginIndex=0&api_key=RGAPI-83c309f0-873a-4a16-8073-01898b18f42a"


def get_match_history(
    puuID: str, APIKey: str, amount: int = 200, step: int = 100
) -> list:
    history_lenght = np.arange(0, amount, step)
    history_list = []
    for startIndex in history_lenght:
        count = step
        URL = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?queue=450&start={}&count={}&api_key={}".format(
            puuID, startIndex, count, APIKey
        )
        response = requests.get(URL)
        if response.status_code != 200:
            logger.debug(response.text)
            break
        json_data = json.loads(response.text)
        history_list.extend(json_data)
    return history_list
