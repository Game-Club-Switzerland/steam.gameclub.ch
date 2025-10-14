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
    
    @staticmethod
    def steamGroupInGamePlayer(groupID64, allPlayerSummaries):
        inGamePlayers = {}
        for player in allPlayerSummaries:
            if allPlayerSummaries[player].get('gameextrainfo'):
                inGamePlayers[player] = allPlayerSummaries[player]
        return inGamePlayers
    
    @staticmethod
    def createSteamProfileWidget(steamProfile):
        return f"""<a href="https://steamcommunity.com/profiles/{steamProfile['steamid']}" target="_blank" style="text-decoration:none;color:#66c0f4;">
            <img src="{steamProfile.get('avatarfull', '')}" alt="{steamProfile.get('personaname', '')}" style="width:24px;height:24px;border-radius:3px;vertical-align:middle;margin-right:6px;" />
            {steamProfile.get('personaname', '')}
        </a>"""