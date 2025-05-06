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

SERVERBROWSER_TF_GAMEMODES = ("vanilla", "24/7", "dm", "gamemode", "jump/surf", "mvm", "social")
SERVERBROWSER_TF_GAMEMODES_NO_MVM = ("vanilla", "24/7", "dm", "gamemode", "jump/surf", "social")
SERVERBROWSER_TF_GAMEMODES_VANILLA = ("vanilla", "24/7")
__SERVERBROWSER_TF_ENDPOINT = "https://serverbrowser.tf/api/servers/all"
NON_VANILLA_TAGS = ("fadetoblack", "friendlyfire", "gravity", "highlander",
                    "nocrits", "norespawntime", "respawntimes", "fixedspread")

REGION_STR = {
    0: "US East",
    1: "US West",
    2: "South America",
    3: "Europe",
    4: "Asia",
    5: "Australia",
    6: "Middle East",
    7: "Africa",
    255: "World",
}

def get_region_str(region: int) -> str:
    resolved_region = REGION_STR.get(region)
    if resolved_region is None:
        return REGION_STR.get("World")
    else:
        return resolved_region

async def fetch_servers(aiohttp_session: aiohttp.ClientSession,
                        game_mode: str, has_user_playing: bool = False) -> list:
    if game_mode not in SERVERBROWSER_TF_GAMEMODES:
        raise ValueError
    params = {"hasUsersPlaying": "1" if has_user_playing else "0", "category": game_mode}
    async with aiohttp_session.get(__SERVERBROWSER_TF_ENDPOINT, params=params) as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.json()
