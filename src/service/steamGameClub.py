import os
import json

class SteamGameClub:
    
    @staticmethod
    def getGamesList():
        # Load games.json and return a dictionary with appid as key
        games_path = os.path.join(os.path.dirname(__file__), '../../docs/games.json')
        if os.path.exists(games_path):
            with open(games_path, 'r', encoding='utf-8') as f:
                gamesList = json.load(f)
            return gamesList
        else:
            return {}
        
    @staticmethod
    def getGameDetails(appid):
        gamesList = SteamGameClub.getGamesList()
        return gamesList.get(str(appid), None)