from flask import Blueprint, current_app, render_template, request, Response
from app.extensions import cache

import time
import socket
import requests

from app.utils.format_a2s import FormatA2S
from app.utils.cvar_name import CvarName
from app.utils.map_name import MapName

bp = Blueprint("info", __name__, url_prefix="/info")

@bp.route("/<server_ip>")
@cache.cached(timeout=5)
def get_info(server_ip):
    server_port = request.args.get("port", default=27015, type=int)

    server_info = FormatA2S.info(server_ip, server_port)
    server_rules_raw = FormatA2S.rules(server_ip, server_port)
    server_rules = CvarName.rules_to_readable_dict(server_rules_raw)
    player_list = FormatA2S.players(server_ip, server_port)
    current_map_raw = server_info.get("map")
    server_tags = ", ".join(server_info.get("tags"))
    server_steam_group = server_rules_raw.get("sv_steamgroup")
    next_map_raw = CvarName.get_next_map(server_rules_raw)

    game_mode = MapName.map_name_to_game_mode(current_map_raw)
    current_map = MapName.map_name_to_readable_name(current_map_raw)
    next_map = MapName.map_name_to_readable_name(next_map_raw)
    next_map_game_mode = MapName.map_name_to_game_mode(next_map_raw)

    for item in player_list:
        item.update({"duration": int(item.get("time"))})
        if time.strftime("%H", time.gmtime(item["time"])) == '00':
            item["time"] = time.strftime("%M:%S", time.gmtime(item["time"]))
        else:
            item["time"] = time.strftime("%H:%M:%S", time.gmtime(item["time"]))

    return render_template("info.html",
                           player_count = server_info.get("player_count"),
                           max_players = server_info.get("max_players"),
                           raw_map_name = server_info.get("map"),
                           server_ip = socket.gethostbyname(server_ip),
                           server_port = server_port,
                           player_list = player_list,
                           server_rules = server_rules,
                           server_tags = server_tags,
                           server_steam_group = server_steam_group,
                           server_name = server_info.get("name"),
                           current_map = current_map,
                           game_mode = game_mode,
                           next_map = next_map,
                           next_map_game_mode = next_map_game_mode)

@bp.route("/thumbnail/<map_name>")
@cache.cached(timeout=3600)
def get_map_thumbnail(map_name) -> str:
    teamwork_secret_key = current_app.config["TEAMWORK_TF_SECRET_KEY"]
    response = requests.get("https://teamwork.tf/api/v1/map-stats/mapthumbnail/{}?key={}".format(map_name, teamwork_secret_key))
    thumbnail_url = response.json().get("thumbnail")
    if thumbnail_url is not None:
        return Response(thumbnail_url, mimetype='text/plain')
    else:
        return Response(status=404)
