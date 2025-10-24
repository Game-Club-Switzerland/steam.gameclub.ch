import os
import steamGameClub
import steamGameClubWidget

class SteamGameClubMarkdown:
    
    @staticmethod
    def createMarkdownFile(gameDetails):
        if not gameDetails:
            return ""
        
        markdown = f"## {gameDetails.get('name', 'Unknown Game')}\n\n"
        markdown += f"**App ID:** {gameDetails.get('steam_appid', 'N/A')}\n\n"
        markdown += f"**Type:** {gameDetails.get('type', 'N/A')}\n\n"
        markdown += f"**Developers:** {', '.join(gameDetails.get('developers', []))}\n\n"
        markdown += f"**Publishers:** {', '.join(gameDetails.get('publishers', []))}\n\n"
        markdown += f"**Release Date:** {gameDetails.get('release_date', {}).get('date', 'N/A')}\n\n"
        markdown += f"**Description:**\n{gameDetails.get('detailed_description', 'No description available.')}\n\n"
        
        if 'header_image' in gameDetails:
            markdown += f"![Header Image]({gameDetails['header_image']})\n\n"
        
        if 'screenshots' in gameDetails:
            for screenshot in gameDetails['screenshots']:
                markdown += f"![Screenshot]({screenshot['path_full']})\n\n"
        
        return markdown

    @staticmethod
    def getAppDetailsHtmlTd(appid):
        createTd = ""
        SteamGameClub = steamGameClub.SteamGameClub.getGameDetails(appid)
        if SteamGameClub:
            if SteamGameClub.get('img_icon_url', ''):
                createTd = f"<td><a href=\"/game/{appid}\"><img src=\"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{SteamGameClub.get('img_icon_url', '')}.jpg\" alt=\"{SteamGameClub.get('name', '')}\" style=\"width:32px;height:32px;border-radius:4px;\" /></a></td>\n"
                createTd += f"<td><a href=\"/game/{appid}\">{SteamGameClub.get('name', '')}</a></td>\n"
            else:
                createTd = f"<td></td>\n"
                createTd += f"<td><a href=\"/game/{appid}\">{SteamGameClub.get('name', '')}</a></td>\n"
        else:
            createTd = f"<td></td>\n"
            createTd += f"<td><a href=\"/game/{appid}\">{appid}</a></td>\n"
        return createTd

    @staticmethod
    def createMarkdownFileGamesIndex(gameListwithAllPlayTime, allPlayerSummaries):
        print("Creating Markdown file for games...")

        output_dir = os.path.join(os.path.dirname(__file__), '../../docs')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'games.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Games\n\n")
            f.write(SteamGameClubMarkdown.getNavigationGames())
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
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
                f.write(SteamGameClubMarkdown.getAppDetailsHtmlTd(playerPlaytime))
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
        
    @staticmethod
    def createMarkdownFileGames2WeekIndex(gameListwithRecentlyPlayTime, allPlayerSummaries):
        print("Creating Markdown file for games...")

        output_dir = os.path.join(os.path.dirname(__file__), '../../docs')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'games2weeks.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Games\n\n")
            f.write(SteamGameClubMarkdown.getNavigationGames())
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th>2 Weeks</th>
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
            for playerPlaytime in gameListwithRecentlyPlayTime:
                print (playerPlaytime)
                f.write(f"<tr>\n")
                f.write(SteamGameClubMarkdown.getAppDetailsHtmlTd(playerPlaytime))
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_2weeks', '')}</td>\n")
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_forever', '')}</td>\n")
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_windows_forever', '')}</td>\n")
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_mac_forever', '')}</td>\n")
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_linux_forever', '')}</td>\n")
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_deck_forever', '')}</td>\n")
                f.write(f"<td>{len(gameListwithRecentlyPlayTime[playerPlaytime].get('player', []))}</td>\n")
                #f.write(f"<td>{', '.join(gameListwithAllPlayTime[playerPlaytime].get('player', []))}</td>\n")
                players = gameListwithRecentlyPlayTime[playerPlaytime].get('player', [])
                player_html = ''.join([
                    f"<a href=\"{allPlayerSummaries[p].get('profileurl', '')}\" target=\"_blank\" style=\"text-decoration:none;color:#66c0f4;\">"
                    f"<img src=\"{allPlayerSummaries[p].get('avatarfull', '')}\" alt=\"{allPlayerSummaries[p].get('personaname', '')}\" style=\"width:24px;height:24px;border-radius:3px;vertical-align:middle;margin-right:6px;\" />"
                    f"</a>"
                    for p in players if p in allPlayerSummaries
                ])
                f.write(f"<td>{player_html}</td>\n")
                f.write(f"</tr>\n")
            f.write(f"</tbody>\n</table>\n")
        print("Markdown file 'games2weeks.md' created.")
        
    @staticmethod
    def createSteamProfileWidget(steamProfile):
        return f"""<a href="https://steamcommunity.com/profiles/{steamProfile['steamid']}" target="_blank" style="text-decoration:none;color:#66c0f4;">
            <img src="{steamProfile.get('avatarfull', '')}" alt="{steamProfile.get('personaname', '')}" style="width:24px;height:24px;border-radius:3px;vertical-align:middle;margin-right:6px;" />
            {steamProfile.get('personaname', '')}
        </a>"""

    @staticmethod
    def createMarkdownFileGroupInGamePlayer(groupID64, inGamePlayers):
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'ingame.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Steam Group - Members - In-Game\n\n")
            if len(inGamePlayers) == 0:
                f.write(f"<p>Niemand ist im Spiel.</p>\n")
            else:
                f.write("""<table id="charts-table" class="display" style="width:100%">
            <thead>
                <tr>
                    <th>Avatar</th>
                    <th>Name</th>
                    <th>Steam Profile</th>
                    <th>Game</th>
                    <th>Game ID</th>
                </tr>
            </thead>
            <tbody>
        """)
                if len(inGamePlayers) == 0:
                    f.write(f"<tr>\n")
                    f.write(f"<td></td>\n")
                    f.write(f"<td>Niemand ist im Spiel</td>\n")
                    f.write(f"<td></td>\n")
                    f.write(f"<td></td>\n")
                    f.write(f"</tr>\n")
                else:
                    for player in inGamePlayers:
                        f.write(f"<tr>\n")
                        f.write(f"<td><img src=\"{inGamePlayers[player].get('avatarfull', '')}\" alt=\"Avatar\" style=\"width:48px;height:48px;border-radius:4px;\"></td>\n")
                        f.write(f"<td><a href=\"/player/{player}\">{inGamePlayers[player].get('personaname')}</a></td>\n")
                        f.write(f"<td><a href=\"{inGamePlayers[player].get('profileurl', '')}\" target=\"_blank\">Profil</a></td>\n")
                        f.write(f"<td>{inGamePlayers[player].get('gameextrainfo', 'N/A')}</td>\n")
                        f.write(f"<td><a href=\"/game/{inGamePlayers[player].get('gameid', 'N/A')}\" target=\"_blank\">{inGamePlayers[player].get('gameid', 'N/A')}</a></td>\n")
                        f.write(f"</tr>\n")
                        #f.write(f"<div>{steamGameClub.SteamGameClub.createSteamProfileWidget(inGamePlayers[player])}</div>\n")
                        #f.write(f"<br/>\n")
                f.write(f"</tbody>\n</table>\n")
        print("Markdown file 'ingame.md' created.")
    
    @staticmethod
    def createMarkdownFileGroupGames(steamGroup64ID, steamGroup, gameListwithAllPlayTime, allPlayerSummaries):
        print("Creating Markdown file for group games...")
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', steamGroup64ID)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'games.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Games\n\n")
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
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
                f.write(SteamGameClubMarkdown.getAppDetailsHtmlTd(playerPlaytime))
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
    
    @staticmethod
    def createMarkdownFileGroupIndex(groupID64, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames):
        if not steamGroup['members']:
            print("No members found.")
            return
        print(f"Fetched {len(steamGroup['members'])} members.")
        
        steamGroupWidgetHtml = steamGameClubWidget.SteamGameClubWidget.steamGroupWidget(steamGroup)

        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'index.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# {steamGroup['groupName']} - Members\n\n")
            f.write(f"<div class=\"grid cards\" markdown>\n\n")
            f.write(f"- :material-gamepad-variant: [Games](games.md)\n\n")
            f.write(f"- :video_game: [In-Game](ingame.md)\n\n")
            f.write(f"- :material-play: [Playtime](playtime.md)\n\n")
            f.write(f"- :material-timer-play: [Playtime 2 Weeks](playtime2weeks.md)\n\n")
            f.write(f"</div>\n")
            f.write(f"{steamGroupWidgetHtml}\n\n")
            f.write(f"""<table id="charts-table" class="display" style="width:100%">""")
            f.write(f"""<thead>
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
                if player in allPlayerGetOwnedGames:
                    print (player)
                    f.write(f"""<tr>
                        <td><img src="{allPlayerSummaries[player].get('avatarfull')}" alt="Avatar" style="width:48px;height:48px;border-radius:4px;"></td>
                        <td><a href="/player/{player}">{allPlayerSummaries[player].get('personaname')}</a></td>
                        <td>{allPlayerSummaries[player].get('steamid')}</td>
                        <td><a href="{allPlayerSummaries[player].get('profileurl')}" target="_blank">Profil</a></td>""")
                    if 'game_count' in allPlayerGetOwnedGames[player]:
                        f.write(f"""
                        <td>{allPlayerGetOwnedGames[player].get('game_count', '')}</td>""")
                    else:
                        f.write(f"""
                            <td></td>
                        </tr>
                        """)
            f.write("""
        </tbody>
    </table>""")
        print("Markdown file Group 'index.md' created.")
        
    @staticmethod
    def createMarkdownFilePlayerIndex(allPlayerSummaries, allPlayerGetOwnedGames):
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'players.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Player \n\n")
            f.write(f"""<table id="charts-table" class="display" style="width:100%">""")
            f.write(f"""<thead>
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
                f.write(f"""<tr>
                    <td><a href="{allPlayerSummaries[player].get('profileurl')}" target="_blank"><img src="{allPlayerSummaries[player].get('avatarfull')}" alt="Avatar" style="width:48px;height:48px;border-radius:4px;"></a></td>
                    <td><a href="/player/{player}">{allPlayerSummaries[player].get('personaname')}</a></td>
                    <td>{allPlayerSummaries[player].get('steamid')}</td>
                    <td><a href="{allPlayerSummaries[player].get('profileurl')}" target="_blank">Steam Profil</a></td>
                    <td>{allPlayerGetOwnedGames[player].get('game_count', '')}</td>
                </tr>
                """)
            f.write("""
        </tbody>
    </table>""")
        print("Markdown file Player 'player.md' created.")

    def createMarkdownFileGroupPlaytime(groupID64, steamGroup, allPlayerSummaries, allPlayerGetOwnedGames):
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
            
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Player</th>
                <th>Appid</th>
                <th>Forever</th>
                <th>Windows</th>
                <th>Mac</th>
                <th>Linux</th>
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
                        <td><a href="{allPlayerSummaries[playerPlaytime].get('profileurl', '')}" target="_blank">{allPlayerSummaries[playerPlaytime].get('personaname', '')}</a></td>
                        <td><a href="https://steamdb.info/app/{game.get('appid')}">{game.get('appid')}</a></td>
                        <td>{game.get('playtime_forever', '')}</td>
                        <td>{game.get('playtime_windows_forever', '')}</td>
                        <td>{game.get('playtime_mac_forever', '')}</td>
                        <td>{game.get('playtime_linux_forever', '')}</td>
                    </tr>
                    """)
            f.write("""
        </tbody>
    </table>""")
        print("Markdown file 'playtime.md' created.")
        
    def createMarkdownFileGroupPlaytime2Week(groupID64, steamGroup, allPlayerSummaries, allPlayerGetRecentlyPlayedGames):
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
            
            f.write("""<table id="charts-table" class="display" style="width:100%">
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
                                f.write(f"""<tr>
                        <td><a href="{allPlayerSummaries[playerPlaytime].get('profileurl', '')}" target="_blank">{allPlayerSummaries[playerPlaytime].get('personaname', '')}</a></td>
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

    def createMarkdownFileAppDetails(appid, gameListwithAllPlayTime, allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames):
        gameDetails = steamGameClub.SteamGameClub.getGameDetails(appid)
        
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/game/', str(appid))
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'index.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            if gameDetails:
                if gameDetails.get('img_icon_url', ''):
                    f.write(f"#  <a href=\"https://steamdb.info/app/{appid}\"><img src=\"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{gameDetails.get('img_icon_url', '')}.jpg\" alt=\"{gameDetails.get('name', '')}\" style=\"width:32px;height:32px;border-radius:4px;\" /> {gameDetails.get('name', '')}</a>\n\n")
                else:
                    f.write(f"# <a href=\"https://steamdb.info/app/{appid}\">{gameDetails.get('name', '')}</a>\n\n")
            else:
                f.write(f"# <a href=\"https://steamdb.info/app/{appid}\">{appid}</a>\n\n")
            f.write(f"**App ID:** {appid}\n\n")
            f.write(f"## Playtime\n\n")
            f.write(f"**Forever:** {gameListwithAllPlayTime.get('playtime_forever', '')}\n\n")
            f.write(f"**Windows:** {gameListwithAllPlayTime.get('playtime_windows_forever', '')}\n\n")
            f.write(f"**Mac:** {gameListwithAllPlayTime.get('playtime_mac_forever', '')}\n\n")
            f.write(f"**Linux:** {gameListwithAllPlayTime.get('playtime_linux_forever', '')}\n\n")
            f.write(f"**Deck:** {gameListwithAllPlayTime.get('playtime_deck_forever', '')}\n\n")
            f.write(f"**Anzahl Players:** {len(gameListwithAllPlayTime.get('player', []))}\n")
            f.write(f"## {len(gameListwithAllPlayTime.get('player', []))} Player\n\n")
            if gameListwithAllPlayTime.get('player', []):
                f.write("""<table id="charts-table" class="display" style="width:100%">
            <thead>
                <tr>
                    <th></th>
                    <th>Name</th>
                    <th>SteamID</th>
                    <th>Profile</th>
                    <th>Playtime Forever</th>
                    <th>Windows</th>
                    <th>Mac</th>
                    <th>Linux</th>
                    <th>Deck</th>
                    <th>Last Played</th>
                    <th>Playtime 2 Weeks</th>
                </tr>
            </thead>
            <tbody>
        """)
                for player in gameListwithAllPlayTime.get('player', []):
                    f.write(f"<tr>\n")
                    f.write(f"<td><a href=\"{allPlayerSummaries[player].get('profileurl')}\" target=\"_blank\"><img src=\"{allPlayerSummaries[player].get('avatarfull')}\" alt=\"Avatar\" style=\"width:48px;height:48px;border-radius:4px;\"></a></td>")
                    f.write(f"<td><a href=\"/player/{player}\">{allPlayerSummaries[player].get('personaname')}</a></td>")
                    f.write(f"<td>{allPlayerSummaries[player].get('steamid')}</td>")
                    f.write(f"<td><a href=\"{allPlayerSummaries[player].get('profileurl')}\" target=\"_blank\">Steam Profil</a></td>")
                    if allPlayerGetOwnedGames[player]:
                        if allPlayerGetOwnedGames[player]['games']:
                            # find in Array item with appid
                            game = next((g for g in allPlayerGetOwnedGames[player]['games'] if g.get('appid') == appid), None)
                            if game:
                                f.write(f"<td>{game.get('playtime_forever', 0)}</td>")
                                f.write(f"<td>{game.get('playtime_windows_forever', 0)}</td>")
                                f.write(f"<td>{game.get('playtime_mac_forever', 0)}</td>")
                                f.write(f"<td>{game.get('playtime_linux_forever', 0)}</td>")
                                f.write(f"<td>{game.get('playtime_deck_forever', 0)}</td>")
                                f.write(f"<td>{game.get('rtime_last_played', 0)}</td>")
                            else:
                                f.write(f"<td></td>")
                    if allPlayerGetRecentlyPlayedGames[player]:
                        if 'games' in allPlayerGetRecentlyPlayedGames[player]:
                            if allPlayerGetRecentlyPlayedGames[player]['games']:
                                game = next((g for g in allPlayerGetRecentlyPlayedGames[player]['games'] if g.get('appid') == appid), None)
                                if game:
                                    f.write(f"<td>{game.get('playtime_2weeks', 0)}</td>")
                                else:
                                    f.write(f"<td></td>")
                            else:
                                f.write(f"<td></td>")
                        else:   
                            f.write(f"<td></td>")
                    f.write(f"</tr>\n")
                f.write(f"</tbody>\n</table>\n")
            else:
                f.write(f"<p>Keine Spieler gefunden.</p>\n")
        print(f"Markdown file for App ID {appid} created.")
        
    def createMarkdownFileApps(gameListwithAllPlayTime, allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames):
        for gameData in gameListwithAllPlayTime:
            SteamGameClubMarkdown.createMarkdownFileAppDetails(gameData, gameListwithAllPlayTime[gameData], allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames)

    def createMarkdownFilePlayerDetail(player):
        if not player:
            print("No player data provided.")
            return
        
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/player/', player['steamid'])
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'index.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# {player.get('personaname', 'Unknown Player')}\n\n")
            f.write(f"**SteamID:** {player.get('steamid', 'N/A')}\n\n")
            f.write(f"**Profile:** [Link]({player.get('profileurl', '#')})\n\n")
            if 'avatarfull' in player:
                f.write(f"![Avatar]({player['avatarfull']})\n\n")
            f.write(f"**Real Name:** {player.get('realname', 'N/A')}\n\n")
            if 'loccityid' in player or 'locstatecode' in player or 'loccountrycode' in player:
                f.write("### Location\n\n")
                f.write(f"**Location:** {player.get('loccountrycode', 'N/A')}\n\n")
                f.write(f"**State:** {player.get('locstatecode', 'N/A')}\n\n")
                f.write(f"**City ID:** {player.get('loccityid', 'N/A')}\n\n")
        print(f"Markdown file for player {player.get('personaname', 'Unknown Player')} created.")
        
    @staticmethod
    def getNavigationGames():
        navigationGames = "<div class=\"grid cards\" markdown>\n\n"
        navigationGames += "- :material-gamepad-variant: [Games](games.md)\n\n"
        navigationGames += "- :material-timer-play: [Playtime 2 Weeks](games2weeks.md)\n\n"
        navigationGames += "</div>\n"
        return navigationGames
    
    @staticmethod
    def createMarkdownFileIndexTrends(gameListwithRecentlyPlayTime):
        print("Creating Markdown file for Trends...")

        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/index')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'trends.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Trends\n\n")
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th>Playtime 2 Weeks</th>
                <th>Anzahl Players</th>
            </tr>
        </thead>
        <tbody>
    """)
            # Sort games by playtime_2weeks and take only top 15
            sorted_games = sorted(
                gameListwithRecentlyPlayTime.items(),
                key=lambda x: x[1].get('playtime_2weeks', 0),
                reverse=True
            )[:15]
            
            for playerPlaytime, game_data in sorted_games:
                print (playerPlaytime)
                f.write(f"<tr>\n")
                f.write(SteamGameClubMarkdown.getAppDetailsHtmlTd(playerPlaytime))
                f.write(f"<td>{gameListwithRecentlyPlayTime[playerPlaytime].get('playtime_2weeks', '')}</td>\n")
                f.write(f"<td>{len(gameListwithRecentlyPlayTime[playerPlaytime].get('player', []))}</td>\n")
                f.write(f"</tr>\n")
            f.write(f"</tbody>\n</table>\n")
        print("Markdown file 'index/trends.md' created.")
    
    @staticmethod
    def createMarkdownFileAllPlayerDetails(allPlayerSummaries, allPlayerGetOwnedGames, allPlayerGetRecentlyPlayedGames):
        for player in allPlayerSummaries:
            SteamGameClubMarkdown.createMarkdownFilePlayerDetail(allPlayerSummaries[player], allPlayerGetOwnedGames[player], allPlayerGetRecentlyPlayedGames[player])
    
    @staticmethod
    def createMarkdownFilePlayerDetails(playerSummaries, playerGetOwnedGames, playerGetRecentlyPlayedGames):
        #gameDetails = steamGameClub.SteamGameClub.getGameDetails(appid)
        
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/player/', str(playerSummaries['steamid']))
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'index.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# <a href=\"{playerSummaries.get('profileurl', 'Unknown Player')}\" target=\"_blank\">{playerSummaries.get('personaname', 'Unknown Player')}</a>\n\n")
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th>Playtime Forever</th>
                <th>Windows</th>
                <th>Mac</th>
                <th>Linux</th>
                <th>Deck</th>
                <th>last Played</th>
            </tr>
        </thead>
        <tbody>
    """)
            for playerPlaytime in playerGetOwnedGames['games']:
                f.write(f"<tr>\n")
                f.write(SteamGameClubMarkdown.getAppDetailsHtmlTd(playerPlaytime))
                f.write(f"<td>{playerPlaytime.get('playtime_forever', '')}</td>\n")
                f.write(f"<td>{playerPlaytime.get('playtime_windows_forever', '')}</td>\n")
                f.write(f"<td>{playerPlaytime.get('playtime_mac_forever', '')}</td>\n")
                f.write(f"<td>{playerPlaytime.get('playtime_linux_forever', '')}</td>\n")
                f.write(f"<td>{playerPlaytime.get('playtime_deck_forever', '')}</td>\n")
                f.write(f"<td>{playerPlaytime.get('rtime_last_played', '')}</td>\n")
                f.write(f"</tr>\n")
            f.write(f"</tbody>\n</table>\n")
        print(f"Markdown file for Player ID {playerSummaries.get('steamid')} created.")