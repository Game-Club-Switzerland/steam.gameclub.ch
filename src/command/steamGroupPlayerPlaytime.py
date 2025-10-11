import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

def createMarkdownFile(groupID64, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames):
    if not steamGroup:
        print("No members found.")
        return

    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'playtime.md'), "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("hide:\n")
        f.write("  - navigation\n")
        f.write("  - toc\n")
        f.write("---\n")
        f.write(f"# Steam Group - {steamGroup['groupName']} - Members - Playtime\n\n")
            # Write DataTable HTML header
        
        f.write("""<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css"/>
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<table id="charts-table" class="display" style="width:100%">
    <thead>
        <tr>
            <th>Player</th>
            <th>Appid</th>
            <th>Forever</th>
            <th>Windows</th>
            <th>Mac</th>
            <th>Linux</th>
            <th>Last Played</th>
        </tr>
    </thead>
    <tbody>
""")
        for playerPlaytime in allPlayerGetOwnedGames:
            if allPlayerGetOwnedGames[playerPlaytime]:
                for game in allPlayerGetOwnedGames[playerPlaytime]['games']:
                    #gameDetail = steamWebApi.SteamWebApi().fetchAppDetails(game.get('appid'))
                    #print(gameDetail)
                    f.write(f"""<tr>
                    <td>{allPlayerSummaries[playerPlaytime].get('personaname', '')}</td>
                    <td><a href="https://steamdb.info/app/{game.get('appid')}">{game.get('appid')}</a></td>
                    <td>{game.get('playtime_forever', '')}</td>
                    <td>{game.get('playtime_windows_forever', '')}</td>
                    <td>{game.get('playtime_mac_forever', '')}</td>
                    <td>{game.get('playtime_linux_forever', '')}</td>
                    <td>{game.get('rtime_last_played', '')}</td>
                </tr>
                """)
        f.write("""
    </tbody>
</table>""")
    print("Markdown file 'playtime.md' created.")

def main():
    steamGroup = steamWebApi.SteamWebApi().fetchSteamGroup("103582791430857185")
    allPlayerSummaries = steamWebApi.SteamWebApi().fetchAllPlayerSummaries(steamGroup['members'], STEAMWEBAPIKEY)
    allPlayerGetOwnedGames = steamWebApi.SteamWebApi().fetchAllPlayerGetOwnedGames(steamGroup['members'], STEAMWEBAPIKEY)

    createMarkdownFile("103582791430857185", steamGroup, allPlayerSummaries, allPlayerGetOwnedGames)

            

if __name__ == "__main__":
    main()
