import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi
import steamGameClub
import steamGameClubMarkdown
import steamGameClubWidget

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

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
    allPlayerGetRecentlyPlayedGames = steamWebApi.SteamWebApi().fetchAllPlayerGetRecentlyPlayedGames(steamGroup['members'], STEAMWEBAPIKEY)
    
    gameListwithAllPlayTime = steamWebApi.SteamWebApi().getAllGameDetails(allPlayerSummaries, allPlayerGetOwnedGames)
    gameListwithRecentlyPlayTime = steamWebApi.SteamWebApi().getAllGameRecentlyPlayedDetails(allPlayerSummaries, allPlayerGetRecentlyPlayedGames)

    # In-Game Players
    inGamePlayers = steamGameClub.SteamGameClub.steamGroupInGamePlayer(steamGroup64ID, allPlayerSummaries)
    
    # Index Sites
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileIndexTrends(gameListwithRecentlyPlayTime)
    
    # Indexes Player und Games
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFilePlayerIndex(allPlayerSummaries, allPlayerGetOwnedGames)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGamesIndex(gameListwithAllPlayTime, allPlayerSummaries)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGames2WeekIndex(gameListwithRecentlyPlayTime, allPlayerSummaries)
    
    # Game Groups
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupIndex(steamGroup64ID, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupGames(steamGroup64ID, steamGroup, gameListwithAllPlayTime, allPlayerSummaries)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupInGamePlayer(steamGroup64ID, inGamePlayers)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupPlaytime(steamGroup64ID, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames)
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileGroupPlaytime2Week(steamGroup64ID, steamGroup, allPlayerSummaries, allPlayerGetRecentlyPlayedGames)
    
    # Game Apps
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileApps(gameListwithAllPlayTime, allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames)
    
    # Player Details
    steamGameClubMarkdown.SteamGameClubMarkdown.createMarkdownFileAllPlayerDetails(allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames)

    # Widget
    steamGameClubWidget.steamGameClubWidget.steamGroupWidget(steamGroup)
    steam_group_Javascript_widget(steamGroup)

if __name__ == "__main__":
    main()
