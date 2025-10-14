import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi
import steamGameClub
import steamGameClubMarkdown

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

def steamGroupWidget(steamGroup):
    html = f"""<div class="steam-group-widget" style="background: #171a21; color: #c7d5e0; border-radius: 4px; padding: 16px; font-family: 'Motiva Sans', Arial, Helvetica, sans-serif; max-width: 350px; box-sizing: border-box; width: 100%;">
    <style>
    @media (max-width: 480px) {{
        .steam-group-widget {{
            padding: 10px;
            max-width: 100vw;
            font-size: 16px;
        }}
        .steam-group-widget h3 {{
            font-size: 18px !important;
        }}
        .steam-group-widget img {{
            width: 24px !important;
            height: 24px !important;
            margin-right: 6px !important;
        }}
    }}
    </style>
    <h3 style="margin: 0 0 10px 0; font-size: 20px; font-weight: 700;">
        <a href="https://steamcommunity.com/groups/{steamGroup['groupURL']}" style="color: #66c0f4; text-decoration: none;">
            <img src="{steamGroup['avatarIcon']}" alt="{steamGroup['groupName']} Avatar" style="vertical-align: middle; border-radius: 2px; margin-right: 8px; width: 32px; height: 32px;" />
            {steamGroup['groupName']}
        </a>
    </h3>
    <div style="margin-bottom: 4px;">
        <span style="color: #66c0f4; font-weight: 500;">{steamGroup['memberCount']} Mitglieder insgesamt</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #c7d5e0;">{steamGroup['memberOnline']} online</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #59bf40;">{steamGroup['memberInGame']} im Spiel</span>
    </div>
    <div>
        <span style="color: #c7d5e0;">{steamGroup['memberInChat']} im Chat - 
            <a href="https://steamcommunity.com/chat/invite/IQhgcbIe" style="color: #66c0f4; text-decoration: underline;">Chat beitreten</a>
        </span>
    </div>
    <div style="height:16px;"></div>
</div>"""
    return html

def steam_group_widget_html(steamGroup):
    html = steamGroupWidget(steamGroup)
    # Ensure the directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{steamGroup['groupID64']}.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

def steam_group_widget_JavaScript(steamGroup):
    js = f"""<script>
    async function loadSteamGroupWidget() {{
        const response = await fetch('https://steam.gameclub.ch/widget/group/{steamGroup['groupID64']}.html');
        const html = await response.text();
        document.getElementById('steam-group-widget-container').innerHTML = html;
    }}
    document.addEventListener('DOMContentLoaded', loadSteamGroupWidget);
    </script>"""
    #<div id="steam-group-widget-container" style="width:100%;"></div>
    return js

def steam_group_widget_JavaScript_min(groupID64):
    js = f"""<script>async function loadSteamGroupWidget(){{const e=await fetch('https://steam.gameclub.ch/widget/group/{groupID64}.html'),t=await e.text();document.getElementById('steam-group-widget-container').innerHTML=t}}document.addEventListener('DOMContentLoaded',loadSteamGroupWidget);</script>"""
    return js

def steam_group_Javascript_widget(steamGroup):
    js = steam_group_widget_JavaScript_min(steamGroup['groupID64'])
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{steamGroup['groupID64']}.js')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js)
    return js

def fetchAllPlayerSummaries(members):
    all_summaries = []
    for member in members:
        summaries = steamWebApi.SteamWebApi.fetchGetPlayerSummaries([member], STEAMWEBAPIKEY)
        #print(summaries)
        all_summaries.extend(summaries)
    return all_summaries

def fetchSummaries(groupID64):
    steamGroup = steamWebApi.SteamWebApi.fetchSteamGroup(groupID64)
    if not steamGroup:
        print("No members found.")
        return []
    print(f"Fetched {len(steamGroup)} group members.")

    summaries = steamWebApi.SteamWebApi.fetchGetPlayerSummaries(steamGroup, STEAMWEBAPIKEY)
    return summaries

def createMarkdownFileGroup(groupID64, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames):
    if not steamGroup['members']:
        print("No members found.")
        return
    print(f"Fetched {len(steamGroup['members'])} members.")
    
    steamGroupWidgetHtml = steamGroupWidget(steamGroup)

    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'index.md'), "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("hide:\n")
        f.write("  - navigation\n")
        f.write("  - toc\n")
        f.write("---\n")
        f.write(f"# {steamGroup['groupName']} - Members\n\n")
        f.write(f"{steamGroupWidgetHtml}\n")
        f.write(f"""

[Playtime](playtime.md)

[Playtime 2 Weeks](playtime2weeks.md)

<table id="charts-table" class="display" style="width:100%">
    <thead>
        <tr>
            <th>Avatar</th>
            <th>Name</th>
            <th>SteamID</th>
            <th>Profile</th>
            <th>Games</th>
        </tr>
    </thead>
    <tbody>""")
        for player in allPlayerSummaries:
            print (player)
            
            f.write(f"""<tr>
                <td><img src="{allPlayerSummaries[player].get('avatarfull')}" alt="Avatar" style="width:48px;height:48px;border-radius:4px;"></td>
                <td>{allPlayerSummaries[player].get('personaname')}</td>
                <td>{allPlayerSummaries[player].get('steamid')}</td>
                <td><a href="{allPlayerSummaries[player].get('profileurl')}" target="_blank">Profil</a></td>
                <td>{allPlayerGetOwnedGames[player].get('game_count', '')}</td>
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
    print("Markdown file Group 'index.md' created.")

def createMarkdownFileGames(gameListwithAllPlayTime, allPlayerSummaries):
    print("Creating Markdown file for group games...")

    output_dir = os.path.join(os.path.dirname(__file__), '../../docs')
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'games.md'), "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("hide:\n")
        f.write("  - navigation\n")
        f.write("  - toc\n")
        f.write("---\n")
        f.write(f"# Games\n\n")
        f.write("""
<table id="charts-table" class="display" style="width:100%">
    <thead>
        <tr>
            <th>Appid</th>
            <th>Forever</th>
            <th>Windows</th>
            <th>Mac</th>
            <th>Linux</th>
            <th>Deck</th>
            <th>Anzahl Players</th>
            <th>Players</th>
        </tr>
    </thead>
    <tbody>
""")
        for playerPlaytime in gameListwithAllPlayTime:
            print (playerPlaytime)
            f.write(f"<tr>\n")
            SteamGameClub = steamGameClub.SteamGameClub.getGameDetails(playerPlaytime)
            if SteamGameClub:
                if SteamGameClub.get('img_icon_url', ''):
                    f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\"><img src=\"https://media.steampowered.com/steamcommunity/public/images/apps/{playerPlaytime}/{SteamGameClub.get('img_icon_url', '')}.jpg\" alt=\"{SteamGameClub.get('name', '')}\" style=\"width:32px;height:32px;border-radius:4px;\" /></a></td>\n")
                else:
                    f.write(f"<td><a href=\"https://store.steampowered.com/app/{playerPlaytime}\">{SteamGameClub.get('name', '')}</a></td>\n")
            else:
                f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{playerPlaytime}</a></td>\n")
            f.write(f"<td>{gameListwithAllPlayTime[playerPlaytime].get('playtime_forever', '')}</td>\n")
            f.write(f"<td>{gameListwithAllPlayTime[playerPlaytime].get('playtime_windows_forever', '')}</td>\n")
            f.write(f"<td>{gameListwithAllPlayTime[playerPlaytime].get('playtime_mac_forever', '')}</td>\n")
            f.write(f"<td>{gameListwithAllPlayTime[playerPlaytime].get('playtime_linux_forever', '')}</td>\n")
            f.write(f"<td>{gameListwithAllPlayTime[playerPlaytime].get('playtime_deck_forever', '')}</td>\n")
            f.write(f"<td>{len(gameListwithAllPlayTime[playerPlaytime].get('player', []))}</td>\n")
            #f.write(f"<td>{', '.join(gameListwithAllPlayTime[playerPlaytime].get('player', []))}</td>\n")
            players = gameListwithAllPlayTime[playerPlaytime].get('player', [])
            player_html = ''.join([
                f"<a href=\"{allPlayerSummaries[p].get('profileurl', '')}\" target=\"_blank\" style=\"text-decoration:none;color:#66c0f4;\">"
                f"<img src=\"{allPlayerSummaries[p].get('avatarfull', '')}\" alt=\"{allPlayerSummaries[p].get('personaname', '')}\" style=\"width:24px;height:24px;border-radius:3px;vertical-align:middle;margin-right:6px;\" />"
                f"</a>"
                for p in players if p in allPlayerSummaries
            ])
            f.write(f"<td>{player_html}</td>\n")
            f.write(f"</tr>\n")
        f.write(f"</tbody>\n</table>\n")
    print("Markdown file 'games.md' created.")

def main():
    steamGroup64ID = "103582791430857185"
    steamGroup = steamWebApi.SteamWebApi().fetchSteamGroup(steamGroup64ID)
    allPlayerSummaries = steamWebApi.SteamWebApi().fetchAllPlayerSummaries(steamGroup['members'], STEAMWEBAPIKEY)
    allPlayerGetOwnedGames = steamWebApi.SteamWebApi().fetchAllPlayerGetOwnedGames(steamGroup['members'], STEAMWEBAPIKEY)
    
    gameListwithAllPlayTime = steamWebApi.SteamWebApi().getAllGameDetails(allPlayerSummaries, allPlayerGetOwnedGames)

    inGamePlayers = steamGameClub.SteamGameClub.steamGroupInGamePlayer(steamGroup64ID, allPlayerSummaries)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileInGamePlayer(steamGroup64ID, inGamePlayers)
    
    createMarkdownFileGroup(steamGroup64ID, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames)
    createMarkdownFileGames(gameListwithAllPlayTime, allPlayerSummaries)
    steam_group_widget_html(steamGroup)
    steam_group_Javascript_widget(steamGroup)

if __name__ == "__main__":
    main()
