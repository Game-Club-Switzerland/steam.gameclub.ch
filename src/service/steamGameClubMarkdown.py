import os
import steamGameClub

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
                    f.write(f"<td><a href=\"https://steamdb.info/app/{playerPlaytime}\">{SteamGameClub.get('name', '')}</a></td>\n")
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
        print("Markdown file 'steam_games.md' created.")