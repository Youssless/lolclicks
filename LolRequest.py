import requests
import json
import time
from pynput.mouse import Listener
import threading
import datetime as Date

'''
    class that preps the request to be handled
'''
class GenerateRequest:
    def __init__(self, ign):
        self.RGAPI_URL = {
            "summoner":"{proxy}/lol/summoner/{version}/summoners/by-name/{ign}?api_key={api_key}",
            "spectator":"{proxy}/lol/spectator/{version}/active-games/by-summoner/{user_id}?api_key={api_key}"
        }

        # load api key from json
        with open("apikey.json") as f:
            k = json.load(f)

        self.ign = ign
        self.api_key=k["key"]
        
        # build summoner url before spectator as specatator url needs summoner id from summoner url
        self.summoner_url = self.__build_url('summoner')
        self.spectator_url = self.__build_url('spectator')

    '''
        param t: takes two types -> spectator, summoner
        builds the urls for requests
    '''
    def __build_url(self, t):
        try:
            url = self.RGAPI_URL[t].format(
                proxy="https://euw1.api.riotgames.com",
                version="v4",
                ign=self.ign if t=='summoner' else None,
                user_id=self.request_id() if t=='spectator' else None,
                api_key=self.api_key
            )
        except KeyError as e:
            print("Username or API key does not exist, cannot request summoner " + str(e))
            print("Make sure to enter summoner username correctly next time")
            print("Visit https://developer.riotgames.com/ to generate API key")
            return None

        return url

    
    '''
        returns the id from summoner json
    '''
    def request_id(self):
        summoner_json = requests.get(self.summoner_url)
        return summoner_json.json()['id']

    '''
        returns the status code of the spectator url.#
        404 = player not in game
        200 = player in game
    '''
    def request_status_code(self):
        try:
            spectator_json = requests.get(self.spectator_url)
            print(self.summoner_url)
            print(self.spectator_url)
            time.sleep(5)
        except requests.RequestException as e:
            print(e)
            return -1

        return spectator_json.status_code
    
    '''
        param t: takes two types -> spectator, summoner
        returns the summoner json or spectator json
    '''
    def request_json(self, t):
        if t == 'summoner':
            summoner_json = requests.get(self.summoner_url)
            return summoner_json.json()
        elif t == 'spectator':
            spectator_json = requests.get(self.spectator_url)
            return spectator_json


'''
    class that handles the generated request
'''
class LoLRequest:
    def __init__(self, ign, listener):
        self.ign = ign
        self.generate_request = GenerateRequest(self.ign)
        self.listener = listener
        self.count = 0

    '''
        handles the request, checks if the summoner is initially in game or not
        also handles the request of check_summoner_status() function
    '''
    def handle_request(self):
        code = self.generate_request.request_status_code()
        summoner_status = self.check_summoner_status(code)

        # code is -1 when the api key is expired or the username is incorrect.
        # the error is thrown due to not being able to request the summoner id
        if code == -1:
            self.listener.stop()
        
        # game ends once check_summoner_status() returns 404
        if summoner_status == 404:
            print("{0} is currently not in game <{1}>".format(self.ign, summoner_status))
            print("Terminating ... ")
            curr_time = Date.datetime.now()
            with open("num_clicks.log", "a") as f:
                f.write(curr_time.strftime("[%d/%m/%Y %H:%M:%S] ") + str(self.count) + " clicks")
                f.write("\n")
            self.listener.stop()
        elif summoner_status == 403:
            print(self.generate_request.summoner_url)
            print(self.generate_request.spectator_url)
            print(self.generate_request.request_json('spectator'))
            self.listener.stop()

    '''
        param code: reference to the code requested in handle_request()
        returns the status code once the game has ended
    '''
    def check_summoner_status(self, code):
        num_req = 0

        if code == 404:
            return code

        # request loop
        while code == 200:
            code = self.generate_request.request_status_code()
            if code == 404:
                return code
            elif code == 500:
                return code
            elif code == 503:
                return code

            num_req = num_req + 1
            print("{0} is currently in game <{1}>".format(self.ign, code))
            print("Request Count: " + str(num_req))
            print("Click Count: " + str(self.count)+"\n")

