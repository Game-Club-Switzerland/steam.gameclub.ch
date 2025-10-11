import os
import sys
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

# https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de

# Create and Update GameList.json by Player GetRecentlyPlayedGames

def getGameList(gameListbyPlayer):
    gameList = {}
    for player in gameListbyPlayer:
        if gameListbyPlayer[player] and 'games' in gameListbyPlayer[player]:
            for game in gameListbyPlayer[player]['games']:
                appid = str(game['appid'])
                if appid not in gameList:
                    gameList[appid] = {
                        'appid': appid,
                        'name': game.get('name', ''),
                        'img_icon_url': game.get('img_icon_url', ''),
                    }
    return gameList

def main():
    steamGroup = steamWebApi.SteamWebApi().fetchSteamGroup("103582791430857185")
    gameListbyPlayer = steamWebApi.SteamWebApi().fetchAllPlayerGetRecentlyPlayedGames(steamGroup['members'], STEAMWEBAPIKEY)
    
    gameList = getGameList(gameListbyPlayer)
    
    # check if games.json exists
    if os.path.exists(os.path.join(os.path.dirname(__file__), '../../docs/games.json')):
        with open(os.path.join(os.path.dirname(__file__), '../../docs/games.json'), 'r', encoding='utf-8') as f:
            existing_game_list = json.load(f)
            
        # Backup existing games.json with timestamp and in folder
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(os.path.dirname(__file__), '../../docs/game/backup', f'{timestamp}.json')
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(existing_game_list, f, ensure_ascii=False, indent=4)
        print(f"Backup of existing games.json created at {backup_path}")
        
        # Merge existing data with new data
        for game in gameList.items():
            print(game)
            appid = game[0]
            if appid not in existing_game_list:
                existing_game_list[appid] = game[1]

        with open(os.path.join(os.path.dirname(__file__), '../../docs/games.json'), 'w', encoding='utf-8') as f:
            json.dump(existing_game_list, f, ensure_ascii=False, indent=4)
    else:
        
        with open(os.path.join(os.path.dirname(__file__), '../../docs/games.json'), 'w', encoding='utf-8') as f:
            json.dump(gameList, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()