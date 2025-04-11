from enum import Enum
import aiohttp

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
    
    @classmethod
    def _missing_(cls, _):
        return cls.WORLD

class ServerList:
    SERVERBROWSER_TF_GAMEMODES = ("vanilla", "24/7", "dm", "gamemode", "jump/surf", "mvm", "social")
    __SERVERBROWSER_TF_ENDPOINT = "https://serverbrowser.tf/api/servers/all"
    NON_VANILLA_TAGS = ("fadetoblack", "friendlyfire", "gravity", "highlander", "nocrits", "norespawntime", "respawntimes")

    @classmethod
    async def fetch_servers(cls, aiohttp_session: aiohttp.ClientSession, game_mode: str) -> list:
        if game_mode not in cls.SERVERBROWSER_TF_GAMEMODES:
            raise ValueError
        params = {"hasUsersPlaying": "0", "category": game_mode}
        async with aiohttp_session.get(cls.__SERVERBROWSER_TF_ENDPOINT, params=params) as r:
            if r.status != 200:
                r.raise_for_status()
            return await r.json()
