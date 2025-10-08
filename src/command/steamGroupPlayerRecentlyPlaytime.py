import requests
import os
import sys

import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAM_GROUP_URL = "https://steamcommunity.com/gid/103582791430857185/memberslistxml/?xml=1"
STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

def fetch_steam_group_members():
    response = requests.get(STEAM_GROUP_URL)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    members = []
    for member in root.findall('members/steamID64'):
        members.append(member.text)
    return members

def fetch_steam_player_summaries(steam_ids):
    if not steam_ids:
        return []
    ids_string = ",".join(steam_ids)
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMWEBAPIKEY}&steamids={ids_string}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("response", {}).get("players", [])

def fetch_steam_player_GetOwnedGames(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAMWEBAPIKEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("response", {}).get("games", [])

def fetchAllPlayerGetRecentlyPlayedGames(members):
    allPlayerGetRecentlyPlayedGames = {}
    for member in members:
        print(f"Fetching recently played games for SteamID: {member}")
        recentlyPlayedGames = steamWebApi.SteamWebApi.fetchGetRecentlyPlayedGames([member], STEAMWEBAPIKEY)
        allPlayerGetRecentlyPlayedGames[member] = recentlyPlayedGames
    return allPlayerGetRecentlyPlayedGames

def createMarkdownFile(groupID64):
    steamGroup = steamWebApi.SteamWebApi().fetch_steam_group_members(groupID64)
    if not steamGroup:
        print("No members found.")
        return
    allPlayerGetRecentlyPlayedGames = fetchAllPlayerGetRecentlyPlayedGames(steamGroup['members'])
    
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'playtime2weeks.md'), "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("hide:\n")
        f.write("  - navigation\n")
        f.write("  - toc\n")
        f.write("---\n")
        f.write(f"# Steam Group - {steamGroup['groupName']} - Members - Playtime 2 Weeks\n\n")
            # Write DataTable HTML header
        
        f.write("""<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css"/>
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<table id="charts-table" class="display" style="width:100%">
    <thead>
        <tr>
            <th>Player</th>
            <th>Appid</th>
            <th>Game Name</th>
            <th>playtime_2weeks</th>
            <th>playtime_forever</th>
            <th>playtime_windows_forever</th>
            <th>playtime_mac_forever</th>
            <th>playtime_linux_forever</th>
            <th>playtime_deck_forever</th>
        </tr>
    </thead>
    <tbody>
""")
        for playerPlaytime in allPlayerGetRecentlyPlayedGames:
            if allPlayerGetRecentlyPlayedGames[playerPlaytime]:
                for game in allPlayerGetRecentlyPlayedGames[playerPlaytime]:
                    print(game)
                    f.write(f"""<tr>
                    <td>{playerPlaytime}</td>
                    <td>{game.get('appid', '')}</td>
                    <td>{game.get('name', '')}</td>
                    <td>{game.get('playtime_2weeks', '')}</td>
                    <td>{game.get('playtime_forever', '')}</td>
                    <td>{game.get('playtime_windows_forever', '')}</td>
                    <td>{game.get('playtime_mac_forever', '')}</td>
                    <td>{game.get('playtime_linux_forever', '')}</td>
                    <td>{game.get('playtime_deck_forever', '')}</td>
                </tr>
                """)
        f.write("""
    </tbody>
</table>
<script>
    $(document).ready(function() {
        $('#steam-members').DataTable({
            "pageLength": 25,
            "language": {
                "url": "//cdn.datatables.net/plug-ins/1.13.6/i18n/de-DE.json"
            }
        });
    });
</script>""")
    print("Markdown file 'playtime2weeks.md' created.")

def main():
    members = fetch_steam_group_members()
    print(f"Fetched {len(members)} group members.")
    if members:
        summaries = fetch_steam_player_summaries(members[:5])  # Fetch summaries for first 5 members as a sample
        for summary in summaries:
            print(f"Player: {summary.get('personaname')} (SteamID: {summary.get('steamid')})")
            games = fetch_steam_player_GetOwnedGames(summary.get('steamid'))
            print(f"  Owns {len(games)} games.")
            

if __name__ == "__main__":
    createMarkdownFile("103582791430857185")
