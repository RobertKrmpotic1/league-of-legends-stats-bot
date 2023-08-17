import requests
import pandas as pd
import json

# find account id
def getaccountID(summonerName, APIKey):
    URL = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(
        summonerName, APIKey
    )
    basic_response = requests.get(URL)
    json_data = json.loads(basic_response.text)
    basic_df = pd.DataFrame.from_dict(json_data, orient="index")
    basic_df = basic_df.transpose()
    basic_df.index = basic_df["name"]
    return basic_df["accountId"][0], basic_df["puuid"][0]
