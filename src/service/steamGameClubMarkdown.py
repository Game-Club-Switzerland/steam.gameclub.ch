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
    def createMarkdownFileGamesIndex(gameListwithAllPlayTime, allPlayerSummaries):
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
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Appid</th>
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
                SteamGameClub = steamGameClub.SteamGameClub.getGameDetails(playerPlaytime)
                if SteamGameClub:
                    if SteamGameClub.get('img_icon_url', ''):
                        f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\"><img src=\"https://media.steampowered.com/steamcommunity/public/images/apps/{playerPlaytime}/{SteamGameClub.get('img_icon_url', '')}.jpg\" alt=\"{SteamGameClub.get('name', '')}\" style=\"width:32px;height:32px;border-radius:4px;\" /></a></td>\n")
                        f.write(f"<td>{SteamGameClub.get('name', '')}</td>\n")
                    else:
                        f.write(f"<td></td>\n")
                        f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{SteamGameClub.get('name', '')}</a></td>\n")
                else:
                    f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{playerPlaytime}</a></td>\n")
                    f.write(f"<td></td>\n")
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
        print("Markdown file 'steam_games.md' created.")
        
    @staticmethod
    def createSteamProfileWidget(steamProfile):
        return f"""<a href="https://steamcommunity.com/profiles/{steamProfile['steamid']}" target="_blank" style="text-decoration:none;color:#66c0f4;">
            <img src="{steamProfile.get('avatarfull', '')}" alt="{steamProfile.get('personaname', '')}" style="width:24px;height:24px;border-radius:3px;vertical-align:middle;margin-right:6px;" />
            {steamProfile.get('personaname', '')}
        </a>"""

    @staticmethod
    def createMarkdownFileInGamePlayer(groupID64, inGamePlayers):
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', groupID64)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'ingame.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Steam Group - Members - In-Game\n\n")
            for player in inGamePlayers:
                print (player)
                print (inGamePlayers[player])
                f.write(f"{steamGameClub.SteamGameClub.createSteamProfileWidget(inGamePlayers[player])}\n")
                f.write(f"<br/>\n")
        print("Markdown file 'ingame.md' created.")
    
    @staticmethod
    def createMarkdownFileGroupGames(steamGroup64ID, steamGroup, gameListwithAllPlayTime, allPlayerSummaries):
        print("Creating Markdown file for group games...")
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/', steamGroup64ID)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'games.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("#  - navigation\n")
            f.write("  - toc\n")
            f.write("---\n")
            f.write(f"# Games\n\n")
            f.write("""<table id="charts-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Appid</th>
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
                SteamGameClub = steamGameClub.SteamGameClub.getGameDetails(playerPlaytime)
                if SteamGameClub:
                    if SteamGameClub.get('img_icon_url', ''):
                        f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\"><img src=\"https://media.steampowered.com/steamcommunity/public/images/apps/{playerPlaytime}/{SteamGameClub.get('img_icon_url', '')}.jpg\" alt=\"{SteamGameClub.get('name', '')}\" style=\"width:32px;height:32px;border-radius:4px;\" /></a></td>\n")
                        f.write(f"<td>{SteamGameClub.get('name', '')}</td>\n")
                    else:
                        f.write(f"<td></td>\n")
                        f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{SteamGameClub.get('name', '')}</a></td>\n")
                else:
                    f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{playerPlaytime}</a></td>\n")
                    f.write(f"<td></td>\n")
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
            f.write("#  - toc\n")
            f.write("---\n")
            f.write(f"# {steamGroup['groupName']} - Members\n\n")
            f.write(f"{steamGroupWidgetHtml}\n\n")
            f.write(f"[Games](games.md)\n\n")
            f.write(f"[In-Game](ingame.md)\n\n")
            f.write(f"[Playtime](playtime.md)\n\n")
            f.write(f"[Playtime 2 Weeks](playtime2weeks.md)\n\n")
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
    </table>""")
        print("Markdown file Group 'index.md' created.")
        
    @staticmethod
    def createMarkdownFilePlayerIndex(allPlayerSummaries, allPlayerGetOwnedGames):
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs')
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f'player.md'), "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("hide:\n")
            f.write("  - navigation\n")
            f.write("#  - toc\n")
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
    </table>""")
        print("Markdown file Player 'player.md' created.")