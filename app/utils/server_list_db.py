from flask import Flask
from urllib.parse import urlsplit

from app.extensions import db, steamutils
from app.models.server import Server
from .server_list import ServerList, ServerRegions

import socket

NON_VANILLA_TAGS = ("fadetoblack", "friendlyfire", "gravity", "highlander", "nocrits", "norespawntime", "respawntimes")

def parse_hostname(server_addr: str) -> tuple:
    parsed = urlsplit("//" + server_addr)
    return parsed.hostname, parsed.port

def populate_server_db(app: Flask) -> None:
    server = Server()
    with app.app_context():
        for game_mode in ServerList.SERVERBROWSER_TF_GAMEMODES:
            server_raw = ServerList.fetch_servers(game_mode)
            for item in server_raw:
                server_addr = parse_hostname(item.get("ip"))
                server_ip = socket.gethostbyname(server_addr[0])
                server_port = server_addr[1]
                steam_server_info = steamutils.get_server_info(server_ip, server_port)
                if steam_server_info is None:
                    continue
                server_steamid = steam_server_info.get("steamid")
                server_vac = steam_server_info.get("secure")
                server.server_steam_id = server_steamid
                server.server_ip = server_ip
                server.server_port = server_port
                server.location = ServerRegions(item.get("region"))
                server.server_name = item.get("name")
                server.server_map = item.get("map")
                server.max_players = item.get("maxPlayers")
                server.vac = server_vac
                server.sourcetv = True if steam_server_info.get("specport") else False
                server.vanilla = False
                if game_mode == "vanilla" or game_mode == r'24/7':
                    if not any(i in item.get("keywords") for i in NON_VANILLA_TAGS):
                        server.vanilla = True
                db.session.add(server)
        db.session.commit()
