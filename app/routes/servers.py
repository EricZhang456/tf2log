from flask import Blueprint, render_template, request, Response
from enum import Enum
from app.extensions import limiter, cache

import asyncio, aiohttp

from app.utils.parse_hostname import parse_hostname
from app.utils.param_bool import param_bool
from app.utils.server_list import ServerList, ServerRegions
from app.utils.map_utils import MapUtils

bp = Blueprint("servers", __name__, url_prefix="/servers")

class GamePresets(Enum):
    VANILLA = 1
    SEMI_VANILLA = 2
    CUSTOM = 3
    ALL = 4

    @classmethod
    def _missing_(cls, _):
        return cls.VANILLA

@bp.route("/")
@limiter.limit("90 per minute")
@cache.cached(timeout=5, query_string=True)
async def get_server_list():
    has_user_playing = request.args.get("has_user_playing", default=True, type=param_bool)
    not_full = request.args.get("not_full", default=False, type=param_bool)
    no_password = request.args.get("password", default=False, type=param_bool)
    region_param = request.args.get("region", default=-1, type=int)
    region = None if region_param == -1 else ServerRegions(region_param)
    vanilla = GamePresets(request.args.get("vanilla", default=1, type=int))
    alltalk = request.args.get("alltalk", default=False, type=param_bool)
    nocrits = request.args.get("nocrits", default=False, type=param_bool)
    gravity = request.args.get("gravity", default=False, type=param_bool)
    increased_maxplayers = request.args.get("increased_maxplayers", default=False, type=param_bool)
    respawntimes = request.args.get("respawntimes", default=False, type=param_bool)
    friendlyfire = request.args.get("friendlyfire", default=False, type=param_bool)
    dmgspread = request.args.get("dmgspread", default=False, type=param_bool)
    norespawntime = request.args.get("norespawntime", default=False, type=param_bool)
    replay = request.args.get("replay", default=False, type=param_bool)
    server_list_raw = []
    server_list = []
    game_mode_list = (ServerList.SERVERBROWSER_TF_GAMEMODES_VANILLA 
                    if vanilla == GamePresets.VANILLA or vanilla == GamePresets.SEMI_VANILLA 
                    else ServerList.SERVERBROWSER_TF_GAMEMODES_NO_MVM)
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item, has_user_playing))
                       for item in game_mode_list]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_list_raw.extend(item)
    for item in server_list_raw:
        server_tags = tuple(item.get("keywords").split(","))
        server_addr = parse_hostname(item.get("ip"))
        if ((region and region != ServerRegions(item.get("region")))
            or (not_full and (item.get("players") == item.get("maxPlayers")))
            or (no_password and item.get("visibility") != 0)
            or (alltalk and "alltalk" not in server_tags)
            or (nocrits and "nocrits" not in server_tags)
            or (gravity and "gravity" not in server_tags)
            or (increased_maxplayers and "increased_maxplayers" not in server_tags)
            or (norespawntime and "norespawntime" not in server_tags)
            or (respawntimes and "respawntimes" not in server_tags)
            or (dmgspread and "dmgspread" not in server_tags)
            or (friendlyfire and "friendlyfire" not in server_tags)
            or (replay and "replays" not in server_tags)):
            continue
        vanilla_status = GamePresets.VANILLA
        if any(i in server_tags for i in ServerList.NON_VANILLA_TAGS):
            vanilla_status = GamePresets.SEMI_VANILLA
        if MapUtils.map_name_to_game_mode(item.get("map")) is None:
            vanilla_status = GamePresets.CUSTOM
        match vanilla_status:
            case GamePresets.VANILLA:
                vanilla_str = "Vanilla"
            case GamePresets.SEMI_VANILLA:
                vanilla_str = "Custom Vanilla"
            case GamePresets.CUSTOM:
                vanilla_str = "Custom"
        if vanilla != vanilla_status and vanilla != GamePresets.ALL:
            continue
        server_list.append({"name": item.get("name"), 
                            "ip": item.get("ip"),
                            "addr": server_addr[0],
                            "port": server_addr[1],
                            "password": item.get("visibility"),
                            "tags": ", ".join(server_tags),
                            "region": ServerList.get_region_str(item.get("region")),
                            "vanilla": vanilla_str,
                            "raw_map": item.get("map"),
                            "game_mode": MapUtils.map_name_to_game_mode(item.get("map")),
                            "map": MapUtils.map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("maxPlayers"),
                            "bots": item.get("bots")})
    subview_header = request.headers.get("x-fetch-subview")
    if subview_header is not None and (subview_header.isnumeric() and int(subview_header) == 1):
        return render_template("servers_item.html", show_server_list = True, server_list = server_list)
    else:
        return render_template("servers.html", server_list = server_list)

@bp.route("/favorites")
@limiter.limit("90 per minute")
@cache.cached(timeout=5)
def get_favorites():
    return render_template("servers.html", show_server_list = False)

@bp.route("/server_count")
@limiter.limit("90 per minute")
@cache.cached(timeout=600)
async def get_server_count():
    server_count = 0
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item, False)) 
                       for item in (ServerList.SERVERBROWSER_TF_GAMEMODES_NO_MVM)]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_count += len(item)
    return Response(str(server_count), mimetype="text/plain")

@bp.route("/player_count")
@limiter.limit("90 per minute")
@cache.cached(timeout=300)
async def get_player_count():
    player_count = 0
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item, False)) 
                       for item in (ServerList.SERVERBROWSER_TF_GAMEMODES_NO_MVM)]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        for server in item:
            player_count += server.get("players") - server.get("bots")
    return Response(str(player_count), mimetype="text/plain")
