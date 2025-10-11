import os
import sys

import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

def createMarkdownFile(groupID64, steamGroup, allPlayerSummaries, allPlayerGetRecentlyPlayedGames):
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
            <th>2 Weeks</th>
            <th>Forever</th>
            <th>Windows</th>
            <th>Mac</th>
            <th>Linux</th>
            <th>Deck</th>
        </tr>
    </thead>
    <tbody>
""")
        for playerPlaytime in allPlayerGetRecentlyPlayedGames:
            if allPlayerGetRecentlyPlayedGames[playerPlaytime]:
                    if 'games' in allPlayerGetRecentlyPlayedGames[playerPlaytime]:
                        for game in allPlayerGetRecentlyPlayedGames[playerPlaytime]['games']:
                    #gameDetail = steamWebApi.SteamWebApi().fetchAppDetails(game.get('appid'))
                            f.write(f"""<tr>
                    <td>{allPlayerSummaries[playerPlaytime].get('personaname', '')}</td>
                    <td><a href="https://steamdb.info/app/{game.get('appid', '')}">{game.get('appid', '')}</a></td>
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
</table>""")
    print("Markdown file 'playtime2weeks.md' created.")

def main(groupID64):
    steamGroup = steamWebApi.SteamWebApi().fetchSteamGroup(groupID64)
    if not steamGroup:
        print("No members found.")
        return

    allPlayerSummaries = steamWebApi.SteamWebApi().fetchAllPlayerSummaries(steamGroup['members'], STEAMWEBAPIKEY)

    allPlayerGetRecentlyPlayedGames = steamWebApi.SteamWebApi().fetchAllPlayerGetRecentlyPlayedGames(steamGroup['members'], STEAMWEBAPIKEY)
    
    createMarkdownFile(groupID64, steamGroup, allPlayerSummaries, allPlayerGetRecentlyPlayedGames)

if __name__ == "__main__":
    main("103582791430857185")
