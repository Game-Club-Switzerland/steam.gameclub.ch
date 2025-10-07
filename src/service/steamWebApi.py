import requests
import xml.etree.ElementTree as ET

class SteamWebApi:
    
    @staticmethod
    def fetch_steam_group_members(groupID64):
        url = f"https://steamcommunity.com/gid/{groupID64}/memberslistxml/?xml=1"
        response = requests.get(url)
        if response.status_code == 200:
            steamGroup = {}
            root = ET.fromstring(response.content)
            steamGroup['members'] = []
            for member in root.findall('members/steamID64'):
                steamGroup['members'].append(member.text)
            steamGroup['groupID64'] = root.findtext('groupID64')
            steamGroup['groupName'] = root.findtext('groupDetails/groupName')
            steamGroup['memberCount'] = root.findtext('groupDetails/memberCount')
            steamGroup['memberInGame'] = root.findtext('groupDetails/membersInGame')
            steamGroup['memberInChat'] = root.findtext('groupDetails/membersInChat')
            steamGroup['memberOnline'] = root.findtext('groupDetails/membersOnline')
            steamGroup['avatarIcon'] = root.findtext('groupDetails/avatarIcon')
            steamGroup['groupURL'] = root.findtext('groupDetails/groupURL')
            return steamGroup
        else:
            response.raise_for_status()
    
    @staticmethod
    def fetch_steam_player_summaries(steamids, api_key):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={','.join(steamids)}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['response']['players']
        else:
            response.raise_for_status()
            
    @staticmethod
    def fetch_steam_player_GetOwnedGames(steamids, api_key):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'games' in response.json()['response']:
                return response.json()['response']['games']
        else:
            response.raise_for_status()