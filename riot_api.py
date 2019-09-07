import json
import pprint
import time as time

import requests as requests

class RiotAPI:
    """This static class contains methods and associated data relevant to
    interacting with the League of Legends API

    ----------------------------------------------------------------------"""

    api_key = ""
    patch = "9.14"
    region = "na1"
    regions = ['ru', 'kr', 'br1', 'oc1', 'jp1', 'na1', 'eun1', 'euw1', 'tr1', 'la1', 'la2']
    regions.sort()

    @staticmethod
    def init():
        RiotAPI.set_api_key()
        print("Enter your region:")
        for reg in RiotAPI.regions:
            print("- " + reg)
        RiotAPI.region = input()
        while RiotAPI.region not in RiotAPI.regions:
            RiotAPI.region = input("Invalid Region\nEnter your region:")

    @staticmethod
    def set_api_key():
        new_key = input("Enter a new API key: ")
        RiotAPI.api_key = new_key
        
        #Test validity of API key by using a known API url
        test_res = requests.get("https://na1" + RiotAPI.player_by_summoner_base
         + "sharp104?api_key=" + RiotAPI.api_key)
        test_res = test_res.json()
        print(test_res)

        if "status" in test_res.keys():
            print("Invalid API key")
            RiotAPI.set_api_key()

        print()

    @staticmethod
    def make_request(url):
        """Just requests.get with extra decoding and status handline
        Returns in format of a Python dictionary"""
        result = requests.get(url)

        result = RiotAPI.handle_error(url, result)
        
        return(result)

    @staticmethod
    def handle_error(url, result):
        """Checks all data to ensure it's received properly without an error code

        In cases where an unexpected status code is received, handle_error 
        takes appropriate action. Typical cases include when the API server
        times out and when rate limit is exceeded."""

        while result.status_code != 200:
            code = result.status_code

            #If statements to handle all kinds of errors
            if code == 200:
                #Request was successful
                return(result.json())
            elif code == 400:
                raise Exception("Bad Request")
            elif code == 401:
                print("Error: Unauthorized")
                RiotAPI.set_api_key()
            elif code == 403:
                raise Exception("Forbidden")
            elif code == 404:
                #TODO: Explore better handling of this case
                return {}
            elif code == 415:
                raise Exception("Unsupported Media Type")
            elif code == 429:
                print("Too many requests, pausing...")
                time.sleep(30)
                result = requests.get(url)
            elif code == 500:
                print("Internal Server Error")
                time.sleep(60)
                result = requests.get(url)
            elif code == 503:
                print("Service Unavailable")
                time.sleep(60)
                result = requests.get(url)


        return(result.json())

    #URLs
    
    #LEAGUE-V4
    challengers_base = ".api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"

    #MATCH-V4
    matchlist_by_id_base = ".api.riotgames.com/lol/match/v4/matchlists/by-account/"
    match_by_number_base = ".api.riotgames.com/lol/match/v4/matches/"
    timeline_by_number_base = ".api.riotgames.com/lol/match/v4/timelines/by-match/"

    #SUMMONER-V4
    player_by_summoner_base = ".api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    

    @staticmethod
    def get_player_by_summoner(name):
        """Returns a player's encrypted Summoner ID given a username"""

        name = name.strip().lower()
        url = "https://" + RiotAPI.region + RiotAPI.player_by_summoner_base + name
        url += "?api_key=" + RiotAPI.api_key
        encrypted_id = RiotAPI.make_request(url)["accountId"]
        return(encrypted_id)

    @staticmethod
    def get_matchlist_by_id(encrypted_id):
        """Returns a player's recent matches given an Encrypted Summoner ID

        Parameters:
        encrypted_id: a player's encrypted Summoner ID

        Returns:
        matchlist: list of the given player's 100 most recent match numbers"""

        url = "https://" + RiotAPI.region + RiotAPI.matchlist_by_id_base + encrypted_id
        url += "?api_key=" + RiotAPI.api_key
        matchlist = RiotAPI.make_request(url)["matches"]
        return(matchlist)

    @staticmethod
    def get_match_by_number(match_num):
        """Returns a match data dictionary given a match number"""

        url = "https://" + RiotAPI.region + RiotAPI.match_by_number_base + str(match_num)
        url += "?api_key=" + RiotAPI.api_key
        raw = RiotAPI.make_request(url)
        match = raw
        return(match)

    @staticmethod
    def get_timeline_by_number(match_num):
        """Returns a match timeline dictionary given a match number"""

        url = "https://" + RiotAPI.region + RiotAPI.timeline_by_number_base + str(match_num)
        url += "?api_key=" + RiotAPI.api_key
        raw = RiotAPI.make_request(url)
        timeline = raw
        return timeline

    @staticmethod
    def get_challengers():
        """Returns a list of the Summoner Names of all challenger players
        in a region"""

        url = "https://" + RiotAPI.region + RiotAPI.challengers_base
        url += "?api_key=" + RiotAPI.api_key
        challengers_raw = RiotAPI.make_request(url)
        challengers_list = []
        for entry in challengers_raw["entries"]:
            challengers_list.append(entry['summonerName'])
        return(challengers_list)

      #CSV Conversion
    @staticmethod
    def match_to_csv_line(match, csv_file_path):
        print("This should do something, eventually")

# Necessary Initialization
RiotAPI.init()