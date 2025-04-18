from flask import Flask

import socket, aiohttp

class SteamUtils:
    __STEAMWORKS_SEVRER_LIST_ENDPOINT = "https://api.steampowered.com/IGameServersService/GetServerList/v1/"

    def __init__(self) -> None:
        self.steamworks_api_key: str | None = None

    def init_app(self, app: Flask) -> None:
        self.steamworks_api_key = app.config.get("STEAMWORKS_SECRET_KEY")

    async def get_server_info(self,
                              aiohttp_session:aiohttp.ClientSession,
                              server_addr: str, server_port: int) -> dict | None:
        server_ip = socket.gethostbyname(server_addr)
        query_params = {
            "key": self.steamworks_api_key,
            "filter": f"\\gameaddr\\{server_ip}:{server_port}",
            "limit": "1",
        }
        async with aiohttp_session.get(self.__STEAMWORKS_SEVRER_LIST_ENDPOINT,
                                       params=query_params) as r:
            if r.status != 200:
                r.raise_for_status()
            else:
                result_raw = await r.json()
                result = result_raw.get("response")
                if result:
                    return ((result.get("servers"))[0])
                else:
                    return None
