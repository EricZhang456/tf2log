from flask import Flask
from urllib.parse import urlsplit

from .server_list import ServerList, ServerRegions

NON_VANILLA_TAGS = ("fadetoblack", "friendlyfire", "gravity", "highlander", "nocrits", "norespawntime", "respawntimes")

#def populate_server_db(app: Flask) -> None:
#    with app.app_context():
#        for game_mode in ServerList.SERVERBROWSER_TF_GAMEMODES:
#            server_raw = ServerList.fetch_servers(game_mode)
#            for item in server_raw:
#                server = Server()
#                server_addr = item.get("ip")
#                if bool(db.session.query(Server).filter_by(server_addr=server_addr).first()):
#                    continue
#                server.server_addr = server_addr
#                server.server_name = item.get("name").replace("\x01", "")
#                server.max_players = 0 if item.get("maxPlayers") is None else item.get("maxPlayers")
#                server.location = ServerRegions.WORLD if item.get("region") is None else ServerRegions(item.get("region"))
#                server.vanilla = False
#                server.mvm = False
#                if game_mode == "vanilla" or game_mode == r'24/7':
#                    if not any(i in item.get("keywords") for i in NON_VANILLA_TAGS):
#                        server.vanilla = True
#                if game_mode == "mvm":
#                    server.mvm = True
#                db.session.add(server)
#        db.session.commit()
