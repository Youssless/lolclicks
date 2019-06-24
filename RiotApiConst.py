import json

# read the key from the json file
with open("apikey.json") as f:
    k = json.load(f)

RGAPI_URL = {
    "summoner":"{proxy}/lol/summoner/{version}/summoners/by-name/{ign}?api_key={api_key}",
    "spectator":"{proxy}/lol/spectator/{version}/active-games/by-summoner/{user_id}?api_key={api_key}"
}

TOKENS = {
    "proxy":"https://euw1.api.riotgames.com",
    "version":"v4",
    "ign":"veg kx",
    "api_key":k["key"],
    "user_id":"{user_id}"
}
