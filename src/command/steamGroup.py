import requests
import os

import xml.etree.ElementTree as ET

STEAM_GROUP_URL = "https://steamcommunity.com/gid/103582791430857185/memberslistxml/?xml=1"

def fetch_steam_group_members():
    response = requests.get(STEAM_GROUP_URL)
    response.raise_for_status()
    root = ET.fromstring(response.content)
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
    return group_name, members, memberCount, membersInGame, membersInChat, membersOnline, avatarIcon, groupURL

def steam_group_widget():
    group_name, members, memberCount, membersInGame, membersInChat, membersOnline, avatarIcon, groupURL = fetch_steam_group_members()
    html = f"""<div class="steam-group-widget">
    <h3><a href="https://steamcommunity.com/groups/{groupURL}"><img src="{avatarIcon}" alt="{group_name} Avatar" /> {group_name}</a></h3>
    <span style="color: #62a7e3;">{memberCount} Total Members</span><br>
    <span style="color: #62a7e3;">{membersOnline} Online</span><br>
    <span style="color: #8bc53f;">{membersInGame} In Game</span><br>
    <span>{membersInChat} im Chat - <a href="https://steamcommunity.com/chat/invite/IQhgcbIe" style="color: #62a7e3;">Chat beitreten</a></span>
</div>"""
    # Ensure the directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

if __name__ == "__main__":
    steam_group_widget()