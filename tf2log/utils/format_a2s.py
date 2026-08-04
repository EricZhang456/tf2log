"""Utilities related to A2S."""

import a2s
import retry

from .custom_except import NotTF2


@retry.retry(TimeoutError, tries=5, delay=1)
async def info(server_ip: str, server_port: int = 27015) -> dict[str, any]:
    """Get server info formatted in a dictionary.

    :param str server_ip: Server IP.
    :param int server_port: Server port, defaults to 27015.
    :return: A dictionary of the server info.
    :rtype: dict
    """
    server_address = (server_ip, server_port)
    server_info_raw = await a2s.ainfo(server_address)

    if isinstance(server_info_raw, a2s.GoldSrcInfo):
        raise NotTF2()

    server_info = {
        "name": server_info_raw.server_name,
        "map": server_info_raw.map_name,
        "folder": server_info_raw.folder,
        "game": server_info_raw.game,
        "player_count": server_info_raw.player_count,
        "max_players": server_info_raw.max_players,
        "bot_count": server_info_raw.bot_count,
        "platform": server_info_raw.platform,
        "password": server_info_raw.password_protected,
        "vac": server_info_raw.vac_enabled,
        "appid": server_info_raw.app_id
    }

    if server_info_raw.keywords:
        server_info["tags"] = filter(None, server_info_raw.keywords.split(","))
    else:
        server_info["tags"] = []

    optional_attrs = ["stv_port"]
    for item in optional_attrs:
        if getattr(server_info_raw, item) is not None:
            server_info.update({item: getattr(server_info_raw, item)})

    return server_info


@retry.retry(TimeoutError, tries=5, delay=1)
async def rules(server_ip: str, server_port: int = 27015) -> dict[str, str]:
    """Get server rules (cvars flagged with notify) formatted in a dictionary

    :param str server_ip: Server IP.
    :param int server_port: Server port, defaults to 27015.
    :return: A dictionary of the server rules.
    :rtype: dict
    """
    server_address = (server_ip, server_port)
    return await a2s.arules(server_address)


@retry.retry(TimeoutError, tries=5, delay=1)
async def players(server_ip: str, server_port: int = 27015) -> list[dict[str], any]:
    """Get server plays formatted in a list of dictionary

    :param str server_ip: Server IP.
    :param int server_port: Server port, defaults to 27015.
    :return: A list dictionary of the players on the server.
    :rtype: list[dict]
    """
    server_address = (server_ip, server_port)
    server_players = []
    server_players_raw = await a2s.aplayers(server_address)

    for item in server_players_raw:
        player = {"name": item.name,
                  "score": item.score,
                  "time": item.duration}
        server_players.append(player)

    return server_players
