import json
import os
import time


from riot_api import RiotAPI

def download_matches(summoner_name, folder):
    print("Downloading Matches for " + summoner_name)
    encrypted_id = RiotAPI.get_player_by_summoner(summoner_name)
    matchlist = RiotAPI.get_matchlist_by_id(encrypted_id)
    count = 1
    for match_num in matchlist:
        filename = folder + "\\" + str(match_num['gameId']) + ".json"
        if os.path.exists(filename):
            count += 1
            continue

        match_num = match_num['gameId']
        
        match_data_general = RiotAPI.get_match_by_number(match_num)
        match_data_timeline = RiotAPI.get_timeline_by_number(match_num)

        match_data = {
            'stats': match_data_general,
            'timeline': match_data_timeline,
        }

        with open(filename, 'w') as file:
            json.dump(match_data, file)

        print("Downloaded match " + str(count))
        count += 1

    print()

if __name__ == '__main__':
    import datetime
    
    dt = datetime.datetime.now()
    directory_name = "Data\\Matches " + dt.strftime("%m-%d-%Y") + "\\"
    try:
        os.mkdir(directory_name)
    except:
        pass

    download_matches("Sharp104", directory_name)