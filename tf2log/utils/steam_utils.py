"""Utilities related to Steam."""

from socket import AddressFamily # pylint: disable = no-name-in-module
import aiohttp
import aiodns

from flask import Flask

STEAMWORKS_SERVER_LIST_ENDPOINT = \
    "https://api.steampowered.com/IGameServersService/GetServerList/v1/"


class SteamUtils:
    """Steam utilities class."""

    def __init__(self) -> None:
        self.steamworks_api_key = None

    def init_app(self, app: Flask) -> None:
        """Initialize the Steam utilities object.

        :param Flask app: A Flask object with the STEAMWORKS_SECRET_KEY config
                          pointing to a Steam API key.
        """
        self.steamworks_api_key = app.config.get("STEAMWORKS_SECRET_KEY")

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
        async with aiohttp_session.get(STEAMWORKS_SERVER_LIST_ENDPOINT,
                                       params=query_params) as r:
            if r.status != 200:
                r.raise_for_status()
            else:
                result_raw = await r.json()
                result = result_raw.get("response")
                if result:
                    return ((result.get("servers"))[0])
                return None
