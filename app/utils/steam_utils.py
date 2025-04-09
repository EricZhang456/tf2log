from flask import Flask

import requests
import socket

class SteamUtils:
    __STEAMWORKS_SEVRER_LIST_ENDPOINT = "https://api.steampowered.com/IGameServersService/GetServerList/v1/"

    def __init__(self) -> None:
        self.steamworks_api_key: str | None = None
    
    def init_app(self, app: Flask) -> None:
        self.steamworks_api_key = app.config.get("STEAMWORKS_SECRET_KEY")

    def get_server_info(self, server_addr: str, server_port: int) -> dict | None:
        server_ip = socket.gethostbyname(server_addr)
        query_params = {
            "key": self.steamworks_api_key,
            "filter": f"\\gameaddr\\{server_ip}:{server_port}",
            "limit": "1",
        }
        server_info = requests.get(self.__STEAMWORKS_SEVRER_LIST_ENDPOINT, params=query_params).json().get("response")
        if server_info:
            return ((server_info.get("servers"))[0])
        else:
            return None
