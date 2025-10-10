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
    def fetchGetOwnedGamesCount(steamids, apiKey):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apiKey}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'game_count' in response.json()['response']:
                return response.json()['response']['game_count']
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
    # https://store.steampowered.com/api/appdetails/?appids=570&language=de
    def fetchAppDetails(appid):
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&language=de"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if str(appid) in data and data[str(appid)]['success']:
                return data[str(appid)]['data']
            else:
                return None
        else:
            response.raise_for_status()

    @staticmethod
    # https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de
    def fetchGetAppList():
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['applist']['apps']
        else:
            response.raise_for_status()

    @staticmethod
    def fetchAllPlayerGetOwnedGames(members, apiKey):
        allPlayerGetOwnedGames = {}
        for member in members:
            print(f"Fetching owned games for SteamID: {member}")
            getOwnedGames = SteamWebApi.fetchGetOwnedGames([member], apiKey)
            allPlayerGetOwnedGames[member] = getOwnedGames
        return allPlayerGetOwnedGames
    
    @staticmethod
    def fetchAllPlayerGetOwnedGamesCount(members, apiKey):
        allPlayerGetOwnedGamesCount = {}
        for member in members:
            print(f"Fetching owned games count for SteamID: {member}")
            getOwnedGamesCount = SteamWebApi.fetchGetOwnedGamesCount([member], apiKey)
            allPlayerGetOwnedGamesCount[member] = getOwnedGamesCount
        return allPlayerGetOwnedGamesCount

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
    
    @staticmethod
    def getAllGameDetails(allPlayerSummaries, allPlayerGetOwnedGames):
        allGameDetails = {}
        for player in allPlayerSummaries:
            if allPlayerGetOwnedGames[player]:
                for game in allPlayerGetOwnedGames[player]:
                    appid = game.get('appid')
                    
                    if appid not in allGameDetails:
                        print(f"Fetching app details for AppID: {appid}")
                        appDetails = SteamWebApi.fetchAppDetails(appid)
                        allGameDetails[appid] = {}
                        if appDetails:
                            allGameDetails[appid]['playtime_forever'] = game.get('playtime_forever', '')
                            allGameDetails[appid]['playtime_windows_forever'] = game.get('playtime_windows_forever', 0)
                            allGameDetails[appid]['playtime_mac_forever'] = game.get('playtime_mac_forever', 0)
                            allGameDetails[appid]['playtime_linux_forever'] = game.get('playtime_linux_forever', 0)
                            allGameDetails[appid]['playtime_deck_forever'] = game.get('playtime_deck_forever', 0)
                    else:
                        # Sum playtime if app already exists form all Player
                        allGameDetails[appid]['playtime_forever'] = allGameDetails[appid]['playtime_forever'] + game.get('playtime_forever')
                        allGameDetails[appid]['playtime_windows_forever'] = allGameDetails[appid]['playtime_windows_forever'] + game.get('playtime_windows_forever', 0)
                        allGameDetails[appid]['playtime_mac_forever'] = allGameDetails[appid]['playtime_mac_forever'] + game.get('playtime_mac_forever', 0)
                        allGameDetails[appid]['playtime_linux_forever'] = allGameDetails[appid]['playtime_linux_forever'] + game.get('playtime_linux_forever', 0)
                        allGameDetails[appid]['playtime_deck_forever'] = allGameDetails[appid]['playtime_deck_forever'] + game.get('playtime_deck_forever', 0)
        return allGameDetails
