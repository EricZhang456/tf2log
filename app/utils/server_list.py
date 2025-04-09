from enum import Enum
import requests

class ServerRegions(Enum):
    US_EAST = 0
    US_WEST = 1
    SOUTH_AMERICA = 2
    EUROPE = 3
    ASIA = 4
    AUS = 5
    MIDDLE_EAST = 6
    AFRICA = 7
    WORLD = 255

class ServerList:
    SERVERBROWSER_TF_GAMEMODES = ("vanilla", r'24/7', "dm", "gamemode", r'jump/surf', "mvm", "social")
    SERVERBROWSER_TF_ENDPOINT = "https://serverbrowser.tf/api/servers/all"

    @classmethod
    def fetch_servers(cls, game_mode: str) -> list:
        if game_mode not in cls.SERVERBROWSER_TF_GAMEMODES:
            raise ValueError
        params = {"hasUsersPlaying": "0", "category": game_mode}
        return requests.get(cls.SERVERBROWSER_TF_ENDPOINT, params=params).json()
