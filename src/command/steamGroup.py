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

def main():
    steamGroup64ID = "103582791430857185"
    steamGroup = steamWebApi.SteamWebApi().fetchSteamGroup(steamGroup64ID)
    allPlayerSummaries = steamWebApi.SteamWebApi().fetchAllPlayerSummaries(steamGroup['members'], STEAMWEBAPIKEY)
    allPlayerGetOwnedGames = steamWebApi.SteamWebApi().fetchAllPlayerGetOwnedGames(steamGroup['members'], STEAMWEBAPIKEY)
    
    gameListwithAllPlayTime = steamWebApi.SteamWebApi().getAllGameDetails(allPlayerSummaries, allPlayerGetOwnedGames)

    inGamePlayers = steamGameClub.SteamGameClub.steamGroupInGamePlayer(steamGroup64ID, allPlayerSummaries)
    if inGamePlayers:
        print(f"Found {len(inGamePlayers)} players currently in-game.")
        steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileInGamePlayer(steamGroup64ID, inGamePlayers)
    
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroup(steamGroup64ID, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGames(gameListwithAllPlayTime, allPlayerSummaries)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupGames(steamGroup64ID, steamGroup, gameListwithAllPlayTime, allPlayerSummaries)
    steam_group_widget_html(steamGroup)
    steam_group_Javascript_widget(steamGroup)

if __name__ == "__main__":
    main()
