import requests
import os

import xml.etree.ElementTree as ET

STEAM_GROUP_URL = "https://steamcommunity.com/gid/103582791430857185/memberslistxml/?xml=1"
STEAMWEBAPIKEY = os.getenv("STEAMWEBAPIKEY")

def fetch_steam_group_members():
    response = requests.get(STEAM_GROUP_URL)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    members = []
    for member in root.findall('members/steamID64'):
        members.append(member.text)
    return members

def fetch_steam_player_summaries(steam_ids):
    if not steam_ids:
        return []
    ids_string = ",".join(steam_ids)
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMWEBAPIKEY}&steamids={ids_string}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("response", {}).get("players", [])

def fetch_steam_player_GetOwnedGames(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAMWEBAPIKEY}&steamid={steam_id}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("response", {}).get("games", [])

def createMarkDonwFile():
    members = fetch_steam_group_members()
    if not members:
        print("No members found.")
        return
    summaries = fetch_steam_player_summaries(members)
    with open("steam_players.md", "w", encoding="utf-8") as f:
        f.write("# Steam Group Members\n\n")
        for summary in summaries:
            f.write(f"## {summary.get('personaname')} (SteamID: {summary.get('steamid')})\n")
            f.write(f"- Profile URL: {summary.get('profileurl')}\n")
            f.write(f"- Avatar: ![Avatar]({summary.get('avatarfull')})\n")
            games = fetch_steam_player_GetOwnedGames(summary.get('steamid'))
            f.write(f"- Owns {len(games)} games.\n\n")
    print("Markdown file 'steam_players.md' created.")

def main():
    members = fetch_steam_group_members()
    print(f"Fetched {len(members)} group members.")
    if members:
        summaries = fetch_steam_player_summaries(members[:5])  # Fetch summaries for first 5 members as a sample
        for summary in summaries:
            print(f"Player: {summary.get('personaname')} (SteamID: {summary.get('steamid')})")
            games = fetch_steam_player_GetOwnedGames(summary.get('steamid'))
            print(f"  Owns {len(games)} games.")
            

if __name__ == "__main__":
    