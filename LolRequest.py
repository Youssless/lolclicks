import requests
import json
import time
from pynput.mouse import Listener
import threading
import datetime as Date

class GenerateRequest:
    def __init__(self, ign):
        self.RGAPI_URL = {
            "summoner":"{proxy}/lol/summoner/{version}/summoners/by-name/{ign}?api_key={api_key}",
            "spectator":"{proxy}/lol/spectator/{version}/active-games/by-summoner/{user_id}?api_key={api_key}"
        }

        with open("apikey.json") as f:
            k = json.load(f)

        self.ign = ign
        self.api_key=k["key"]
        self.summoner_url = self.__build_url('summoner')
        self.spectator_url = self.__build_url('spectator')

    def __build_url(self, t):
        url = self.RGAPI_URL[t].format(
            proxy="https://euw1.api.riotgames.com",
            version="v4",
            ign=self.ign if t=='summoner' else None,
            user_id=self.request_id() if t=='spectator' else None,
            api_key=self.api_key
        )
        return url

    def request_id(self):
        summoner_json = requests.get(self.summoner_url)
        return summoner_json.json()['id']

    def request_status_code(self):
        try:
            spectator_json = requests.get(self.spectator_url)
            print(self.summoner_url)
            print(self.spectator_url)
            time.sleep(5)
        except KeyError:
            return -1

        return spectator_json.status_code

    def request_json(self, t):
        if t == 'summoner':
            summoner_json = requests.get(self.summoner_url)
            return summoner_json.json()
        elif t == 'spectator':
            spectator_json = requests.get(self.spectator_url)
            return spectator_json


class LoLRequest:
    def __init__(self, ign, listener):
        self.ign = ign
        self.generate_request = GenerateRequest(self.ign)
        self.listener = listener
        self.count = 0

    def handle_request(self):
        code = self.generate_request.request_status_code()
        summoner_status = self.check_summoner_status(code)

            
        if summoner_status == 404:
            print("{0} is currently not in game <{1}>".format(self.ign, code))
            print("Terminating ... ")
            curr_time = Date.datetime.now()
            with open("num_clicks.log", "a") as f:
                f.write(curr_time.strftime("[%d/%m/%Y %H:%M:%S] ") + str(self.count) + " clicks")
                f.write("\n")
            self.listener.stop()
            print(self.listener.isAlive())
        elif summoner_status == 403:
            print(self.generate_request.summoner_url)
            print(self.generate_request.spectator_url)
            print(self.generate_request.request_json('spectator'))
            self.listener.stop()
        

    def check_summoner_status(self, code):
        c = 0

        while code == 200:
            code = self.generate_request.request_status_code()
            if code == 404:
                print(code)
                '''
                self.listener.stop()
                print("{0} is currently not in game <{1}>".format(self.ign, code))
                '''
                return code
            elif code == 500:
                return code
            elif code == 503:
                return code

            print("{0} is currently in game <{1}>".format(self.ign, code))
            c=c+1
            print(str(c))
            print("Clicks: " + str(self.count)+"\n")

