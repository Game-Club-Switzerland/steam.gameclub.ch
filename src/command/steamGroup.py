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

def fetch_steam_group_members(url):
    response = requests.get(url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    groupID64 = root.findtext('groupID64')
    group_name = root.findtext('groupDetails/groupName')
    memberCount = root.findtext('groupDetails/memberCount')
    membersInGame = root.findtext('groupDetails/membersInGame')
    membersInChat = root.findtext('groupDetails/membersInChat')
    membersOnline = root.findtext('groupDetails/membersOnline')
    avatarIcon = root.findtext('groupDetails/avatarIcon')
    groupURL = root.findtext('groupDetails/groupURL')
    members = []
    for member in root.findall('members/steamID64'):
        members.append(member.text)
    return group_name, members, memberCount, membersInGame, membersInChat, membersOnline, avatarIcon, groupURL, groupID64

def steam_group_widget_html():
    group_name, members, memberCount, membersInGame, membersInChat, membersOnline, avatarIcon, groupURL, groupID64 = fetch_steam_group_members(STEAM_GROUP_URL)
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
        <a href="https://steamcommunity.com/groups/{groupURL}" style="color: #66c0f4; text-decoration: none;">
            <img src="{avatarIcon}" alt="{group_name} Avatar" style="vertical-align: middle; border-radius: 2px; margin-right: 8px; width: 32px; height: 32px;" />
            {group_name}
        </a>
    </h3>
    <div style="margin-bottom: 4px;">
        <span style="color: #66c0f4; font-weight: 500;">{memberCount} Mitglieder insgesamt</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #c7d5e0;">{membersOnline} online</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #59bf40;">{membersInGame} im Spiel</span>
    </div>
    <div>
        <span style="color: #c7d5e0;">{membersInChat} im Chat - 
            <a href="https://steamcommunity.com/chat/invite/IQhgcbIe" style="color: #66c0f4; text-decoration: underline;">Chat beitreten</a>
        </span>
    </div>
    <div style="height:16px;"></div>
</div>"""
    # Ensure the directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{groupID64}.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

def steam_group_widget_JavaScript(groupID64):
    js = f"""<script>
    async function loadSteamGroupWidget() {{
        const response = await fetch('https://steam.gameclub.ch/widget/group/{groupID64}.html');
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

def steam_group_Javascript_widget(groupID64):
    js = steam_group_widget_JavaScript_min(groupID64)
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{groupID64}.js')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js)
    return js

def fetchAllPlayerSummaries(members):
    all_summaries = []
    for member in members:
        summaries = steamWebApi.SteamWebApi.fetch_steam_player_summaries([member], STEAMWEBAPIKEY)
        #print(summaries)
        all_summaries.extend(summaries)
    return all_summaries

def fetchSummaries(groupID64):
    steamGroup = steamWebApi.SteamWebApi.fetch_steam_group_members(groupID64)
    if not steamGroup:
        print("No members found.")
        return []
    print(f"Fetched {len(steamGroup)} group members.")

    summaries = steamWebApi.SteamWebApi.fetch_steam_player_summaries(steamGroup, STEAMWEBAPIKEY)
    return summaries

def createMarkdownFile(groupID64):
    steamGroup = steamWebApi.SteamWebApi.fetch_steam_group_members(groupID64)
    if not steamGroup['members']:
        print("No members found.")
        return
    print(f"Fetched {len(steamGroup['members'])} members.")

    summaries = fetchAllPlayerSummaries(steamGroup['members'])

    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/group/')
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f'{groupID64}.md'), "w", encoding="utf-8") as f:
        f.write("# Steam Group Members\n\n")
            # Write DataTable HTML header
        f.write("""<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css"/>
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<table id="steam-members" class="display" style="width:100%">
    <thead>
        <tr>
            <th>Avatar</th>
            <th>Name</th>
            <th>SteamID</th>
            <th>Profile</th>
            <th>Games Owned</th>
        </tr>
    </thead>
    <tbody>""")
        for player in summaries:
            #games = steamWebApi.SteamWebApi.fetch_steam_player_GetOwnedGames(player['steamid'], STEAMWEBAPIKEY)
                f.write(f"""<tr>
                <td><img src="{player.get('avatarfull')}" alt="Avatar" style="width:48px;height:48px;border-radius:4px;"></td>
                <td>{player.get('personaname')}</td>
                <td>{player.get('steamid')}</td>
                <td><a href="{player.get('profileurl')}" target="_blank">Profil</a></td>
                <td><!-- Placeholder for games owned --></td>
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
    print("Markdown file 'steam_players.md' created.")

if __name__ == "__main__":
    steam_group_widget_html()
    steam_group_Javascript_widget("103582791430857185")
    createMarkdownFile("103582791430857185")
