from flask import Flask
from urllib.parse import urlsplit

from app.extensions import db, steamutils
from app.models.server import Server
from .server_list import ServerList, ServerRegions

import socket
from requests.exceptions import SSLError

NON_VANILLA_TAGS = ("fadetoblack", "friendlyfire", "gravity", "highlander", "nocrits", "norespawntime", "respawntimes")

def parse_hostname(server_addr: str) -> tuple:
    parsed = urlsplit("//" + server_addr)
    return parsed.hostname, parsed.port

def populate_server_db(app: Flask) -> None:
    with app.app_context():
        try:
            for game_mode in ServerList.SERVERBROWSER_TF_GAMEMODES:
                server_raw = ServerList.fetch_servers(game_mode)
                for item in server_raw:
                    server = Server()
                    server_addr = parse_hostname(item.get("ip"))
                    server_ip = socket.gethostbyname(server_addr[0])
                    server_port = server_addr[1]
                    steam_server_info = steamutils.get_server_info(server_ip, server_port)
                    if steam_server_info is None:
                        continue
                    server_steamid = steam_server_info.get("steamid")
                    if bool(db.session.query(Server).filter_by(server_steamid=server_steamid).first()):
                        continue
                    server.server_steamid = server_steamid
                    server.server_ip = server_ip
                    server.server_port = server_port
                    server.server_name = item.get("name").replace("\x01", "")
                    server.location = ServerRegions(item.get("region"))
                    server.max_players = item.get("maxPlayers")
                    server.vanilla = False
                    if game_mode == "vanilla" or game_mode == r'24/7':
                        if not any(i in item.get("keywords") for i in NON_VANILLA_TAGS):
                            server.vanilla = True
                    db.session.add(server)
        except SSLError:
            pass

        db.session.commit()
