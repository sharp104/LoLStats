import datetime
import json
import os
import time
import requests

from riot_api import RiotAPI
import fetch_functions as fetch


if __name__ == "__main__":
    #Makes directory to store matches
    dt = datetime.datetime.now()
    directory_name = "Data\\Matches " + dt.strftime("%m-%d-%Y")
    try:
        os.mkdir(directory_name)
    except:
        pass

    challengers = RiotAPI.get_challengers()

    print(challengers)

    for player in challengers:
        fetch.download_matches(player, directory_name)



    #Ensures current API key works, and updates it if necessary

