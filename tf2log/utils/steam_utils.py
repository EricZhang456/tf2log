"""Utilities related to Steam."""

from typing import Iterable
from enum import IntEnum
from ipaddress import IPv4Address
from socket import AddressFamily # pylint: disable = no-name-in-module

import aiohttp
import aiodns
from quart import Quart


class _FakeIpQueryTypes(IntEnum):
    NONE = 0
    INFO = 1
    PLAYERS = 2
    RULES = 3


def _build_nor_server_query(queries: Iterable[str], use_nand: bool = False):
    return f"{"\\nor\\" if not use_nand else "\\nand\\"}{str(len(queries))}{"".join(queries)}"


class SteamUtils:
    """Steam utilities class."""

    def __init__(self) -> None:
        self.steamworks_api_key = None

    def init_app(self, app: Quart) -> None:
        """Initialize the Steam utilities object.

        :param Quart app: A Flask object with the STEAMWORKS_SECRET_KEY config
                          pointing to a Steam API key.
        """
        self.steamworks_api_key = app.config.get("STEAMWORKS_SECRET_KEY")


    async def _make_http_request(self, aiohttp_session: aiohttp.ClientSession, url: str, params: dict) -> dict:
        async with aiohttp_session.get(url, params=params) as r:
            if r.status != 200:
                r.raise_for_status()
            else:
                result_raw = await r.json()
                return result_raw.get("response")


    async def get_server_info(self,
                              aiohttp_session: aiohttp.ClientSession,
                              server_addr: str, server_port: int = 27015) -> dict | None:
        """Get the information of a server.

        :param ClientSession aiohttp_session: An aiohttp client session.
        :param str server_addr: Server IP.
        :param int server_port: Server port, defaults to 27015.
        :return: A dictionary containing the server information, None if the server
                 cannot be found.
        :rtype: dict or None
        """
        async with aiodns.DNSResolver() as resolver:
            serevr_ip_res = await resolver.gethostbyname(server_addr, AddressFamily.AF_INET)
        server_ip = serevr_ip_res.addresses[0]
        query_params = {
            "key": self.steamworks_api_key,
            "filter": f"\\gameaddr\\{server_ip}:{server_port}",
            "limit": "1",
        }
        result = await self._make_http_request(aiohttp_session,
                                               "https://api.steampowered.com/IGameServersService/GetServerList/v1",
                                               query_params)
        if result:
            return result.get("servers")[0]
        return None


    async def get_fake_ip_server_info(self, aiohttp_session: aiohttp.ClientSession,
                                      server_addr: IPv4Address, server_port: int) -> dict | None:
        query_params = {
            "key": self.steamworks_api_key,
            "fake_ip": int(server_addr),
            "fake_port": server_port,
            "app_id": 440,
            "query_type": int(_FakeIpQueryTypes.INFO)
        }
        result_response = await self._make_http_request(aiohttp_session,
                                                        "https://api.steampowered.com/IGameServersService/QueryByFakeIP/v1/", query_params)
        if not result_response:
            return None
        result_data = result_response.get("ping_data")
        ret = {
            "name": result_data.get("server_name"),
            "map": result_data.get("map"),
            "folder": result_data.get("gamedir"),
            "game": result_data.get("game_description"),
            "player_count": result_data.get("num_players"),
            "max_players": result_data.get("max_players"),
            "bot_count": result_data.get("num_bots"),
            "password": result_data.get("password"),
            "vac": result_data.get("secure"),
            "appid": result_data.get("app_id"),
        }
        result_gametype = result_data.get("gametype")
        if result_gametype:
            ret["tags"] = filter(None, result_gametype.split(","))
        result_stv_port = result_data.get("spectator_server_name")
        if result_stv_port:
            ret["stv_port"] = result_stv_port
        return ret


    async def get_fake_ip_server_rules(self, aiohttp_session: aiohttp.ClientSession,
                                       server_addr: IPv4Address, server_port: int) -> dict | None:
        query_params = {
            "key": self.steamworks_api_key,
            "fake_ip": int(server_addr),
            "fake_port": server_port,
            "app_id": 440,
            "query_type": int(_FakeIpQueryTypes.RULES)
        }
        response = await self._make_http_request(aiohttp_session, "https://api.steampowered.com/IGameServersService/QueryByFakeIP/v1/",
                                                 query_params)
        if not response:
            return None
        response_rules = response.get("rules_data").get("rules")
        ret = {}
        for i in response_rules:
            ret[i.get("rule")] = i.get("value")
        return ret


    async def get_fake_ip_server_players(self, aiohttp_session: aiohttp.ClientSession,
                                         server_addr: IPv4Address, server_port: int) -> dict | None:
        query_params = {
            "key": self.steamworks_api_key,
            "fake_ip": int(server_addr),
            "fake_port": server_port,
            "app_id": 440,
            "query_type": int(_FakeIpQueryTypes.PLAYERS)
        }
        response = await self._make_http_request(aiohttp_session, "https://api.steampowered.com/IGameServersService/QueryByFakeIP/v1/",
                                                 query_params)
        if not response:
            return None
        response_players = response.get("players_data")
        players = []
        if response_players:
            players_data = response_players.get("players")
            for i in players_data:
                players.append({
                    "name": i.get("name"),
                    "score": i.get("score"),
                    "time": i.get("time_played")
                })
        return players


    async def fetch_servers(self, aiohttp_session: aiohttp.ClientSession,
                            query_params: Iterable[str] | None = None,
                            additional_nors: Iterable[str] | None = None) -> list[dict]:
        """Fetch a list of servers.

        :param ClientSession aiohttp_session: An aiohttp client session.
        :param Iterable[str] query_params: Additional query parameters
        :param Iterable[str] additional_nors: Additional query parameters to blacklist.
        :return: A list of servers.
        :rtype: list[dict]
        """
        master_server_query_nor = ["\\gametype\\hidden", "\\proxy\\1"]
        if additional_nors:
            master_server_query_nor.extend(additional_nors)
        nor_query_str = _build_nor_server_query(master_server_query_nor)
        additional_params = "".join(query_params) if query_params else ""
        query_str = "\\appid\\440" + additional_params + nor_query_str
        query_params = {
            "key": self.steamworks_api_key,
            "filter": query_str,
            "limit": 200000
        }
        response = await self._make_http_request(aiohttp_session, "https://api.steampowered.com/IGameServersService/GetServerList/v1",
                                                 query_params)
        if not response:
            return []
        return response.get("servers")
