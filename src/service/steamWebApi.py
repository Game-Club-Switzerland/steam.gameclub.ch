import requests
import xml.etree.ElementTree as ET

class SteamWebApi:
    
    @staticmethod
    def fetchSteamGroup(groupID64):
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
    def fetchGetPlayerSummaries(steamids, apiKey):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apiKey}&steamids={','.join(steamids)}"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'players' in response.json()['response'] and len(response.json()['response']['players']) > 0:
                return response.json()['response']['players'][0]
        else:
            response.raise_for_status()
            
    @staticmethod
    def fetchGetOwnedGames(steamids, apiKey):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apiKey}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'games' in response.json()['response']:
                return response.json()['response']['games']
        else:
            response.raise_for_status()
    
    @staticmethod
    def fetchGetRecentlyPlayedGames(steamids, apiKey):
        #https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=STEAMKEY&steamid=76561197966417969&format=json
        url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={apiKey}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'games' in response.json()['response']:
                return response.json()['response']['games']
        else:
            response.raise_for_status()
            pass

    @staticmethod
    def fetchAllPlayerGetOwnedGames(members, apiKey):
        allPlayerGetOwnedGames = {}
        for member in members:
            print(f"Fetching owned games for SteamID: {member}")
            getOwnedGames = SteamWebApi.fetchGetOwnedGames([member], apiKey)
            allPlayerGetOwnedGames[member] = getOwnedGames
        return allPlayerGetOwnedGames

    @staticmethod
    def fetchAllPlayerGetRecentlyPlayedGames(members, apiKey):
        allPlayerGetRecentlyPlayedGames = {}
        for member in members:
            print(f"Fetching recently played games for SteamID: {member}")
            recentlyPlayedGames = SteamWebApi.fetchGetRecentlyPlayedGames([member], apiKey)
            allPlayerGetRecentlyPlayedGames[member] = recentlyPlayedGames
        return allPlayerGetRecentlyPlayedGames
    
    @staticmethod
    def fetchAllPlayerSummaries(members, apiKey):
        allPlayerSummaries = {}
        for member in members:
            print(f"Fetching player summary for SteamID: {member}")
            playerSummary = SteamWebApi.fetchGetPlayerSummaries([member], apiKey)
            allPlayerSummaries[member] = playerSummary
        return allPlayerSummaries