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
        # Create a Steam profile widget similar to steamcommunity.com, including the currently played game
        profile_url = f"https://steamcommunity.com/profiles/{steamProfile['steamid']}"
        avatar_url = steamProfile.get('avatarfull', '')
        persona_name = steamProfile.get('personaname', '')
        game_info = steamProfile.get('gameextrainfo')
        #game_icon = steamProfile.get('gameiconurl', '')  # Optional: if available
        game_appid = steamProfile.get('gameid')  # Optional: if available

        game_html = ""
        if game_info:
                game_html = f"""
                <div style="margin-top:4px;">
                    <span style="font-size:12px;color:#a4d007;">Playing: {game_info}</span>
                </div>
                """

        return f"""
        <div style="background:#171a21;border-radius:4px;padding:8px;display:flex;align-items:center;max-width:320px;">
            <a href="{profile_url}" target="_blank" style="text-decoration:none;display:flex;align-items:center;">
            <img src="{avatar_url}" alt="{persona_name}" style="width:48px;height:48px;border-radius:4px;margin-right:12px;border:2px solid #3a3f4b;" />
            <div>
                <div style="font-weight:bold;color:#c7d5e0;font-size:16px;">{persona_name}</div>
                {game_html}
            </div>
            </a>
        </div>
        """