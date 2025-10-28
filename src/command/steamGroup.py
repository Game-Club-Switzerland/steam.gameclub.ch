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
    steamGameClubWidget.SteamGameClubWidget.steamGroupWidget(steamGroup)
    steamGameClubWidget.SteamGameClubWidget.createJavaScriptFileforImport(steamGroup)
    #steam_group_Javascript_widget(steamGroup)

if __name__ == "__main__":
    main()
