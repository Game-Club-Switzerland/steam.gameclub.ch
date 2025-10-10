import os
import sys

import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '../service/'))
import steamWebApi

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

STEAMWEBAPIKEY = getenv("STEAMWEBAPIKEY")

# https://api.steampowered.com/ISteamApps/GetAppList/v0002/?language=de