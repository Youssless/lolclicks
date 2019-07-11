import requests
import json
import time

class GenerateRequest:


    def __init__(self, ref):
        self.RGAPI_URL = {
            'rgapiurl':'{proxy}/{category}/{version}/{category_by}/{ref}?api_key={api_key}',
            #"summoner":"{proxy}/lol/summoner/{version}/summoners/by-name/{ign}?api_key={api_key}",
            #"spectator":"{proxy}/lol/spectator/{version}/active-games/by-summoner/{user_id}?api_key={api_key}"
        }

        with open("apikey.json") as f:
            k = json.load(f)

        self.proxy = 'https://euw1.api.riotgames.com'
        self.category = 'lol/summoner'
        self.version = 'v4'
        self.category_by = 'summoners/by-name'
        self.ref = ref
        self.api_key = k["key"]

        self.summoner_url = self.__build_url()
        self.spectator_url = None

    def __build_url(self):
        url = self.RGAPI_URL['rgapiurl'].format(
            proxy=self.proxy,
            category=self.category,
            version=self.version,
            category_by=self.category_by,
            ref=self.ref,
            api_key=self.api_key
        )

        return url

    '''
    def request_id(self):
        summoner_json = requests.get(self.summoner_url)
        return summoner_json.json()['id']
    '''

    def request_status_code(self):
        self.set_spectator()
        spectator_json = requests.get(self.spectator_url)
        time.sleep(5)
        return spectator_json.status_code

    def request_json(self):
        summoner_json = requests.get(self.summoner_url)
        return summoner_json.json()

    def set_spectator(self):
        self.category = 'lol/summoner'
        self.category_by = 'active-games/by-summoner'
        self.ref = 'uGSlgOV2k_r---8-a1YdjXWbCzI0yfNUj-dSWqUpzR8j5k4'
        #self.request_json()['id']

        self.spectator_url = self.__build_url()

class LoLRequest:
    def __init__(self, ign):
        self.ign = ign
        self.generate_request = GenerateRequest(self.ign)

    def handle_request(self, listener):
        code = self.generate_request.request_status_code()
        print(code)

        if code == 200:
            checker = self.check_summoner_status(code)
            if checker == 404:
                listener.stop()
        elif code == 404:
            print("{0} is currently not in game <{1}>".format(self.ign, code))
            print("Terminating ... ")
            listener.stop()
        elif code == 403:
            print(self.generate_request.summoner_url)
            print(self.generate_request.spectator_url)
            print(self.generate_request.request_json())
            listener.stop()

    def check_summoner_status(self, code):
        while code == 200:
            if code == 404:
                return code
            elif code == 500:
                return code
            elif code == 503:
                return code

            code = self.generate_request.request_status_code()
            print("{0} is currently in game <{1}>".format(self.ign, code))

            
            



