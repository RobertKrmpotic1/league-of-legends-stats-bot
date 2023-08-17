import json
import requests


def get_items_dict() -> dict:
    # change link once items change
    items_url = "http://ddragon.leagueoflegends.com/cdn/12.20.1/data/en_US/item.json"
    response = requests.get(items_url)
    json_data = json.loads(response.text)
    items_dict = json_data["data"]
    short_items_dict = {}
    for item in items_dict:
        short_items_dict[int(item)] = items_dict[item]["name"]
    return short_items_dict
