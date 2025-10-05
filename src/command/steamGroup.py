import requests
import os

import xml.etree.ElementTree as ET

STEAM_GROUP_URL = "https://steamcommunity.com/gid/103582791430857185/memberslistxml/?xml=1"

def fetch_steam_group_members():
    response = requests.get(STEAM_GROUP_URL)
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

def steam_group_widget():
    group_name, members, memberCount, membersInGame, membersInChat, membersOnline, avatarIcon, groupURL, groupID64 = fetch_steam_group_members()
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

if __name__ == "__main__":
    steam_group_widget()