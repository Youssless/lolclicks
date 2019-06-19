import click
import RiotApiConst as RAC
import requests

def main():
    handle_request()

# p=proxy, v=version, name=lol username, key= riot api key
# returns the json of the request to get the account id
def request_summoner(p, v, name, key):
    response = requests.get(RAC.RGAPI_URL['summoner'].format(
        proxy=p,
        version=v,
        ign=name,
        api_key=key
    ))
    print(response.url)
    return response.json()

# same as the function above however gets the status code using
# the id found in request_summoner json output
def request_spectator(p, v, name, key, id):
    response = requests.get(RAC.RGAPI_URL['spectator'].format(
        proxy=p,
        version=v,
        ign=name,
        api_key=key,
        user_id=id
    ))
    print(response.url)
    return response.status_code

# requests the json and the status codes
# status codes are used to determine if user is in game or not
def handle_request():
    t = RAC.TOKENS
    r_summoner = request_summoner(t["proxy"], t["version"], t["ign"], t["api_key"])
    r_spectator = request_spectator(t["proxy"], t["version"], t["ign"], t["api_key"], r_summoner["id"])

    # 200 means in game
    # 404 means either offline or not in game
    if r_spectator == 200:
        print(t["ign"]+" is in game "+"<"+str(r_spectator)+">")
        click.listen()
    elif r_spectator == 404:
        print(t["ign"] + " is not in game "+"<"+str(r_spectator)+">")


if __name__ == "__main__":
    main()
