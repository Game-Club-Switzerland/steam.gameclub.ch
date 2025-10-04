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
    members = []
    for member in root.findall('members/steamID64'):
        members.append(member.text)
    return group_name, members, memberCount, membersInGame, membersInChat, membersOnline

def steam_group_widget():
    group_name, members, memberCount, membersInGame, membersInChat, membersOnline = fetch_steam_group_members()
    html = f"""
    <div class="steam-group-widget">
        <h3>{group_name}</h3>
        <p>Total Members: {memberCount}</p>
        <p style="color: #62a7e3;">Online: {membersOnline}</p>
        <p style="color: #8bc53f;">In Game: {membersInGame}</p>
        <p>In Chat: {membersInChat}</p>
    </div>
    """
    # Ensure the directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return html

if __name__ == "__main__":
    steam_group_widget()