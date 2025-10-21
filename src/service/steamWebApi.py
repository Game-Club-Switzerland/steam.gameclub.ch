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
    
    @staticmethod
    def fetchGetPlayerSummaries(steamids, apiKey):
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apiKey}&steamids={','.join(steamids)}"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json() and 'players' in response.json()['response'] and len(response.json()['response']['players']) > 0:
                return response.json()['response']['players'][0]
            else:
                return None
        else:
            return None
    
    @staticmethod
    def fetchGetOwnedGames(steamids, apiKey):
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={apiKey}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json():
                return response.json()['response']
            else:
                return {'game_count': 0, 'games': []}
        else:
            return {'game_count': 0, 'games': []}
    
    @staticmethod
    def fetchGetRecentlyPlayedGames(steamids, apiKey):
        #https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=STEAMKEY&steamid=76561197966417969&format=json
        url = f"http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={apiKey}&steamid={','.join(steamids)}&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            if 'response' in response.json():
                return response.json()['response']
            else:
                return {'total_count': 0, 'games': []}
        else:
            return {'total_count': 0, 'games': []}
    
    @staticmethod
    # https://store.steampowered.com/api/appdetails/?appids=570&language=de
    def fetchAppDetails(appid):
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}&language=de"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if str(appid) in data and data[str(appid)]['success']:
                return data[str(appid)]['data']

    @staticmethod
    # https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de
    def fetchGetAppList():
        url = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['applist']['apps']

    @staticmethod
    def fetchAllPlayerGetOwnedGames(members, apiKey):
        allPlayerGetOwnedGames = {}
        for member in members:
            if member:
                print(f"Fetching owned games for SteamID: {member}")
                getOwnedGames = SteamWebApi.fetchGetOwnedGames([member], apiKey)
                if getOwnedGames:
                    allPlayerGetOwnedGames[member] = getOwnedGames
                else:
                    allPlayerGetOwnedGames[member] = {'game_count': 0, 'games': []}
        return allPlayerGetOwnedGames

    @staticmethod
    def fetchAllPlayerGetRecentlyPlayedGames(members, apiKey):
        allPlayerGetRecentlyPlayedGames = {}
        for member in members:
            print(f"Fetching recently played games for SteamID: {member}")
            recentlyPlayedGames = SteamWebApi.fetchGetRecentlyPlayedGames([member], apiKey)
            if recentlyPlayedGames:
                allPlayerGetRecentlyPlayedGames[member] = recentlyPlayedGames
            else:
                allPlayerGetRecentlyPlayedGames[member] = {'total_count': 0, 'games': []}
        return allPlayerGetRecentlyPlayedGames
    
    @staticmethod
    def fetchAllPlayerSummaries(members, apiKey):
        allPlayerSummaries = {}
        for member in members:
            print(f"Fetching player summary for SteamID: {member}")
            playerSummary = SteamWebApi.fetchGetPlayerSummaries([member], apiKey)
            if playerSummary:
                allPlayerSummaries[member] = playerSummary
            else:
                allPlayerSummaries[member] = {'steamid': member}
        return allPlayerSummaries
    
    @staticmethod
    def getAllGameDetails(allPlayerSummaries, allPlayerGetOwnedGames):
        allGameDetails = {}
        for player in allPlayerSummaries:
            if player in allPlayerGetOwnedGames:
                if allPlayerGetOwnedGames[player]:
                    if 'games' in allPlayerGetOwnedGames[player]:
                        for game in allPlayerGetOwnedGames[player]['games']:
                            appid = game.get('appid')
                            if appid not in allGameDetails:
                                print(f"Fetching app details for AppID: {appid}")
                                #appDetails = SteamWebApi.fetchAppDetails(appid)
                                allGameDetails[appid] = {}
                                allGameDetails[appid]['playtime_forever'] = game.get('playtime_forever', '')
                                allGameDetails[appid]['playtime_windows_forever'] = game.get('playtime_windows_forever', 0)
                                allGameDetails[appid]['playtime_mac_forever'] = game.get('playtime_mac_forever', 0)
                                allGameDetails[appid]['playtime_linux_forever'] = game.get('playtime_linux_forever', 0)
                                allGameDetails[appid]['playtime_deck_forever'] = game.get('playtime_deck_forever', 0)
                                allGameDetails[appid]['player'] = [player]
                            else:
                                # Sum playtime if app already exists form all Player
                                allGameDetails[appid]['playtime_forever'] = allGameDetails[appid]['playtime_forever'] + game.get('playtime_forever')
                                allGameDetails[appid]['playtime_windows_forever'] = allGameDetails[appid]['playtime_windows_forever'] + game.get('playtime_windows_forever', 0)
                                allGameDetails[appid]['playtime_mac_forever'] = allGameDetails[appid]['playtime_mac_forever'] + game.get('playtime_mac_forever', 0)
                                allGameDetails[appid]['playtime_linux_forever'] = allGameDetails[appid]['playtime_linux_forever'] + game.get('playtime_linux_forever', 0)
                                allGameDetails[appid]['playtime_deck_forever'] = allGameDetails[appid]['playtime_deck_forever'] + game.get('playtime_deck_forever', 0)
                                allGameDetails[appid]['player'].append(player)
        return allGameDetails

    @staticmethod
    def getAllGameRecentlyPlayedDetails(allPlayerSummaries, allPlayerGetRecentlyPlayedGames):
        allGameDetails = {}
        for player in allPlayerSummaries:
            if player in allPlayerGetRecentlyPlayedGames:
                if allPlayerGetRecentlyPlayedGames[player]:
                    if 'games' in allPlayerGetRecentlyPlayedGames[player]:
                        for game in allPlayerGetRecentlyPlayedGames[player]['games']:
                            appid = game.get('appid')
                            if appid not in allGameDetails:
                                print(f"Fetching app details for AppID: {appid}")
                                #appDetails = SteamWebApi.fetchAppDetails(appid)
                                allGameDetails[appid] = {}
                                allGameDetails[appid]['name'] = game.get('name', 'Unknown Game')
                                allGameDetails[appid]['img_icon_url'] = game.get('img_icon_url', '')
                                allGameDetails[appid]['playtime_2weeks'] = game.get('playtime_2weeks', 0)
                                allGameDetails[appid]['playtime_forever'] = game.get('playtime_forever', 0)
                                allGameDetails[appid]['playtime_windows_forever'] = game.get('playtime_windows_forever', 0)
                                allGameDetails[appid]['playtime_mac_forever'] = game.get('playtime_mac_forever', 0)
                                allGameDetails[appid]['playtime_linux_forever'] = game.get('playtime_linux_forever', 0)
                                allGameDetails[appid]['playtime_deck_forever'] = game.get('playtime_deck_forever', 0)
                                allGameDetails[appid]['player'] = [player]
                            else:
                                # Sum playtime if app already exists form all Player
                                allGameDetails[appid]['playtime_2weeks'] = allGameDetails[appid]['playtime_2weeks'] + game.get('playtime_2weeks', 0)
                                allGameDetails[appid]['playtime_forever'] = allGameDetails[appid]['playtime_forever'] + game.get('playtime_forever', 0)
                                allGameDetails[appid]['playtime_windows_forever'] = allGameDetails[appid]['playtime_windows_forever'] + game.get('playtime_windows_forever', 0)
                                allGameDetails[appid]['playtime_mac_forever'] = allGameDetails[appid]['playtime_mac_forever'] + game.get('playtime_mac_forever', 0)
                                allGameDetails[appid]['playtime_linux_forever'] = allGameDetails[appid]['playtime_linux_forever'] + game.get('playtime_linux_forever', 0)
                                allGameDetails[appid]['playtime_deck_forever'] = allGameDetails[appid]['playtime_deck_forever'] + game.get('playtime_deck_forever', 0)
                                allGameDetails[appid]['player'].append(player)
        return allGameDetails