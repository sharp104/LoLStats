from datetime import datetime
import json
import os
from pprint import pprint

import pandas as pd


def get_patch_no(match_data_raw: dict) -> str:
    flag = False # Flag for first period in patch number

    patch_no = ''

    for char in match_data_raw['gameVersion']:
        if char == '.':
            if flag:
                return patch_no
            flag = True
        patch_no += char

def parse_sr_match_data(match_data_raw: dict) -> list:
    """Takes dictionary of all match data as input, and 
    returns list of ten player stat dictionaries and two 
    team stat dictionaries"""

    general_game_data = {}
    general_game_data['gameid'] = match_data_raw['gameId']
    general_game_data['patchno'] = get_patch_no(match_data_raw)
    general_game_data['gamelength'] = match_data_raw['gameDuration']/60
    
    #Stores 10 player data dictionaries

    data_list = []

    for i in range(0, 10):
        player_data_raw = match_data_raw['participants'][i]
        player_stats_raw = player_data_raw['stats']
        player_data = general_game_data.copy()
        
        player_data['playerid'] = i + 1
        player_data['result'] = 1 if player_stats_raw['win'] else 0
        player_data['k'] = player_stats_raw['kills']
        player_data['d'] = player_stats_raw['deaths']
        player_data['a'] = player_stats_raw['assists']
        player_data['visionwardbuys'] = player_stats_raw['visionWardsBoughtInGame']
        player_data['wardskilled'] = player_stats_raw['wardsKilled']
        player_data['wardsplaced'] = player_stats_raw['wardsPlaced']
        player_data['visionscore'] = player_stats_raw['visionScore']

        #Clean up handling of these two
        player_data['lane'] = player_data_raw['timeline']['lane']
        player_data['role'] = player_data_raw['timeline']['role']

        try:
            player_data['csminat10'] = player_data_raw['timeline']['creepsPerMinDeltas']['0-10']
        except:
            player_data['csminat10'] = None
        try:
            player_data['csmin10to20'] = player_data_raw['timeline']['creepsPerMinDeltas']['10-20']
        except:
            player_data['csmin10to20'] = None
            pass
        player_data['summonerspells'] = [player_data_raw['spell1Id'], player_data_raw['spell2Id']]
        #player_data['champion'] = champions[player_data_raw['championId']]


        data_list.append(player_data)

    return(data_list)

print("Starting")
print(datetime.now())

players_data = []
for filename in os.listdir("Data/Matches 09-04-2019"):
    with open("Data/Matches 09-04-2019/" + filename, 'r') as f: 
    #TODO: More permanent url system than manual edits
        data = json.load(f)

    if data['mapId'] not in [1, 2, 11]:
        continue
    dl = parse_sr_match_data(data)
    players_data += dl

df = pd.DataFrame(players_data)
print(df)

print("Done")
print(datetime.now())