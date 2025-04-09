from flask import Blueprint, current_app, render_template, request, Response, jsonify
from a2s import BrokenMessageError, BufferExhaustedError
from geoip2.errors import AddressNotFoundError
from app.extensions import cache, geoip, limiter

import time
import socket
import requests

from app.utils.format_a2s import FormatA2S
from app.utils.cvar_utils import CvarUtils
from app.utils.map_utils import MapUtils
from app.utils.custom_except import NotTF2, ServerSourceTV

bp = Blueprint("info", __name__, url_prefix="/info")

@bp.route("/<server_ip>")
@limiter.limit("90 per minute")
@cache.cached(timeout=5, query_string=True)
def get_info(server_ip: str):
    if server_ip.startswith("169.254"):
        return render_template("except.html", except_body="SDR Fake IP not supported."), 400
    server_port = request.args.get("port", default=27015, type=int)
    if server_port < 2000 or server_port > 65535:
        return render_template("except.html", except_body="Invalid port number."), 400

    server_ip = socket.gethostbyname(server_ip)
    server_info = FormatA2S.info(server_ip, server_port)

    if server_info.get("appid") != 440:
        raise NotTF2
    if server_port == server_info.get("stv_port"):
        raise ServerSourceTV

    server_rules_raw = FormatA2S.rules(server_ip, server_port)
    player_list = FormatA2S.players(server_ip, server_port)
    server_rules = CvarUtils.rules_to_readable_dict(server_rules_raw)
    current_map_raw = server_info.get("map")
    sourcetv_port = server_info.get("stv_port")
    server_tags = ", ".join(server_info.get("tags"))
    server_steam_group = server_rules_raw.get("sv_steamgroup")
    next_map_raw = MapUtils.resolve_workshop_map_name(CvarUtils.get_next_map(server_rules_raw))
    next_map_workshop_id = MapUtils.get_workshop_map_id(CvarUtils.get_next_map(server_rules_raw))
    location = ""

    try:
        ip_geo = geoip.geoip_reader.city(server_ip)
        state_name = ip_geo.subdivisions.most_specific.name
        city_name = ip_geo.city.name
        country_name = ip_geo.country.name
        if city_name is not None and state_name is not None:
            location = f"{city_name}, {state_name} - {country_name}"
        elif city_name is None and state_name is None:
            location = country_name
        elif city_name is None:
            location = f"{state_name} - {country_name}"
        elif state_name is None:
            location = f"{city_name} - {country_name}"
    except AddressNotFoundError:
        pass

    game_mode = MapUtils.map_name_to_game_mode(current_map_raw)
    current_map = MapUtils.map_name_to_readable_name(current_map_raw)
    next_map = MapUtils.map_name_to_readable_name(next_map_raw)
    next_map_game_mode = MapUtils.map_name_to_game_mode(next_map_raw)

    for item in player_list:
        item.update({"duration": int(item.get("time"))})
        if time.strftime("%H", time.gmtime(item["time"])) == '00':
            item["time"] = time.strftime("%M:%S", time.gmtime(item["time"]))
        else:
            item["time"] = time.strftime("%H:%M:%S", time.gmtime(item["time"]))

    return render_template("info.html",
                           server_name = server_info.get("name").replace("\x01", ""),
                           player_count = server_info.get("player_count"),
                           max_players = server_info.get("max_players"),
                           raw_map_name = server_info.get("map"),
                           bot_count = server_info.get("bot_count"),
                           password = server_info.get("password"),
                           server_ip = server_ip,
                           server_port = server_port,
                           location = location,
                           sourcetv_port = sourcetv_port,
                           player_list = player_list,
                           server_rules = server_rules,
                           server_tags = server_tags,
                           server_steam_group = server_steam_group,
                           current_map = current_map,
                           game_mode = game_mode,
                           next_map = next_map,
                           next_map_game_mode = next_map_game_mode,
                           next_map_workshop_id = next_map_workshop_id)

@bp.route("/thumbnail/<map_name>")
@limiter.limit("90 per minute")
@cache.cached(timeout=3600)
def get_map_thumbnail(map_name: str):
    teamwork_secret_key = current_app.config["TEAMWORK_TF_SECRET_KEY"]
    response = requests.get(f"https://teamwork.tf/api/v1/map-stats/mapthumbnail/{map_name}?key={teamwork_secret_key}")
    thumbnail_url = response.json().get("thumbnail")
    if thumbnail_url is not None:
        return Response(thumbnail_url, mimetype='text/plain')
    else:
        return Response(status=404)
    
@bp.route("/sourcetv/<server_ip>")
@limiter.limit("90 per minute")
@cache.cached(timeout=500, query_string=True)
def get_source_tv(server_ip: str):
    server_port = request.args.get("port", default=27015, type=int)
    server_info = FormatA2S.info(server_ip, server_port)
    sourcetv_port = server_info.get("stv_port")
    if sourcetv_port != server_port:
        return Response(status=400)
    if sourcetv_port is None:
        return Response(status=404)
    sourcetv_info = FormatA2S.info(server_ip, sourcetv_port)
    if sourcetv_info.get("max_players") == 0:
        return Response(status=404)
    else:
        sourcetv_response = {
            "address": f"{server_ip}:{sourcetv_port}",
            "password": sourcetv_info.get("password"),
        }
        return jsonify(sourcetv_response)
        
@bp.errorhandler(NotTF2)
def handle_nottf2(_):        
    return render_template("except.html", except_body="Server is not running TF2."), 404

@bp.errorhandler(ServerSourceTV)
def handle_server_sourcetv(_):        
    return render_template("except.html", except_body="Server is a SourceTV relay."), 400

@bp.errorhandler(socket.timeout)
def handle_timeout(_):
    return render_template("except.html", except_body="Timed out when fetching game server data."), 504

@bp.errorhandler(socket.gaierror)
def handle_invalid_address(_):
    return render_template("except.html", except_body="Invalid server address."), 400

@bp.errorhandler(ConnectionRefusedError)
def handle_conn_refused(_):
    return render_template("except.html", except_body="Cannot connect to game server."), 502

@bp.errorhandler(BrokenMessageError)
@bp.errorhandler(BufferExhaustedError)
def handle_broken_message(_):
    return render_template("except.html", except_body="Cannot decode response from game server."), 502

@bp.errorhandler(OSError)
def handle_general_error(_):
    return render_template("except.html", except_body="Internal server error."), 500
