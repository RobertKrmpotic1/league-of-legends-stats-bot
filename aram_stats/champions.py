import requests
import pandas as pd
from pandas.io.json import json_normalize


def get_champs():
    # getting champion info
    URL2 = "http://ddragon.leagueoflegends.com/cdn/10.9.1/data/en_US/champion.json"
    response = requests.get(URL2)
    champ_dic = [value for value in response.json().values()]
    # removes first 3 items from dict cause theyre obselite
    champ_dic.pop(0)
    champ_dic.pop(0)
    champ_dic.pop(0)

    # turn into dataframe
    champ_df = pd.DataFrame.from_dict(champ_dic)
    champ_df = champ_df.transpose()
    champ_df = json_normalize(champ_df[0])
    champ_df = champ_df[["name", "key"]]

    champ_df["key"] = pd.to_numeric(champ_df["key"], downcast="float")
    champ_df["key"] = champ_df["key"].astype(int)
    champ_df.index = champ_df["key"]
    champ_df = champ_df.drop("key", axis=1)

    # turn series into dictionary (best formatting)
    return champ_df["name"].to_dict()
