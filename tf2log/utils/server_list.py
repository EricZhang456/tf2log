"""Utilities related to fetching server list."""

from enum import Enum

import aiohttp

from tf2log.utils.game_presets import GamePresets
from tf2log.utils.map_utils import map_name_to_game_mode

class ServerRegions(Enum):
    """Enum for the server regions."""
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
_SERVERBROWSER_TF_ENDPOINT = "https://serverbrowser.tf/api/servers/all"
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
    """Get the name of a region.
    
    :param int region: Region value specified in sv_region.
    :return: Name of the region.
    :rtype: str
    """
    resolved_region = REGION_STR.get(region)
    if resolved_region is None:
        return REGION_STR.get("World")
    return resolved_region

async def fetch_servers(aiohttp_session: aiohttp.ClientSession,
                        game_mode: str, has_user_playing: bool = False) -> list[dict]:
    """Fetch a list of servers.
    
    :param ClientSession aiohttp_session: An aiohttp client session.
    :param str game_mode: Game mode string.
    :param bool has_user_playing: Has user playing.
    :return: A list of servers.
    :rtype: list[dict]
    """
    if game_mode not in SERVERBROWSER_TF_GAMEMODES:
        raise ValueError("Invalid game mode")
    params = {"hasUsersPlaying": "1" if has_user_playing else "0", "category": game_mode}
    async with aiohttp_session.get(_SERVERBROWSER_TF_ENDPOINT, params=params) as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.json()


def get_vanilla_status_str(server_tags: tuple, item: dict) -> tuple:
    """Gets the game preset status and string.

    :param tuple server_tags: Tags of the server.
    :param dict item: Server item.
    :return: A tuple of the game preset status and string.
    :rtype: tuple
    """
    vanilla_status = GamePresets.VANILLA
    if any(i in server_tags for i in NON_VANILLA_TAGS):
        vanilla_status = GamePresets.SEMI_VANILLA
    if map_name_to_game_mode(item.get("map")) is None:
        vanilla_status = GamePresets.CUSTOM
    match vanilla_status:
        case GamePresets.VANILLA:
            vanilla_str = "Vanilla"
        case GamePresets.SEMI_VANILLA:
            vanilla_str = "Vanilla Custom"
        case GamePresets.CUSTOM:
            vanilla_str = "Custom"
    return vanilla_status, vanilla_str
