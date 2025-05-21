"""Server list view"""

import asyncio
import aiohttp

from flask import Blueprint, render_template, request, Response, make_response

from tf2log.extensions import limiter, cache, steamutils
from tf2log.utils.game_presets import GamePresets
from tf2log.utils.parse_hostname import parse_hostname
from tf2log.utils.param_bool import param_bool
from tf2log.utils.server_list import (get_region_str, fetch_servers, ServerRegions,
                                      SERVERBROWSER_TF_GAMEMODES_NO_MVM,
                                      SERVERBROWSER_TF_GAMEMODES_VANILLA)
from tf2log.utils.map_utils import map_name_to_game_mode, map_name_to_readable_name
from tf2log.utils.server_list import get_vanilla_status_str

bp = Blueprint("servers", __name__, url_prefix="/servers")

QUERY_PARAMS = ("alltalk", "nocrits", "gravity", "increased_maxplayers", "respawntimes",
                "friendlyfire", "dmgspread", "norespawntime", "replays")

@bp.route("/")
@limiter.limit("90 per minute")
@cache.cached(timeout=5, query_string=True)
async def get_server_list():
    """Main server list view."""
    has_user_playing = request.args.get("has_user_playing", default=True, type=param_bool)
    not_full = request.args.get("not_full", default=False, type=param_bool)
    no_password = request.args.get("password", default=False, type=param_bool)

    region_param = request.args.get("region", default=-1, type=int)
    region = ServerRegions(region_param) if region_param != -1 else None
    vanilla = GamePresets(request.args.get("vanilla", default=1, type=int))

    server_list_raw = []
    server_list = []
    game_mode_list = (SERVERBROWSER_TF_GAMEMODES_VANILLA
                      if vanilla in {GamePresets.VANILLA, GamePresets.SEMI_VANILLA}
                      else SERVERBROWSER_TF_GAMEMODES_NO_MVM)

    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(fetch_servers(session, item, has_user_playing))
                       for item in game_mode_list]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_list_raw.extend(item)

    for item in server_list_raw:
        item: dict
        server_tags = tuple(item.get("keywords").split(","))
        server_addr = parse_hostname(item.get("ip"))
        if region and region != ServerRegions(item.get("region")):
            continue
        if not_full and item.get("players") == item.get("maxPlayers"):
            continue
        if no_password and item.get("visibility") != 0:
            continue
        server_qualified = True
        for param in QUERY_PARAMS:
            if (request.args.get(param, default=False, type=param_bool)
                and param not in server_tags):
                server_qualified = False
                break
        if not server_qualified:
            continue

        vanilla_status = get_vanilla_status_str(server_tags, item)
        if vanilla not in {vanilla_status[0], GamePresets.ALL}:
            continue

        server_list.append({"name": item.get("name"),
                            "ip": item.get("ip"),
                            "addr": server_addr[0],
                            "port": server_addr[1],
                            "password": item.get("visibility"),
                            "tags": ", ".join(server_tags),
                            "region": get_region_str(item.get("region")),
                            "vanilla": vanilla_status[1],
                            "raw_map": item.get("map"),
                            "game_mode": map_name_to_game_mode(item.get("map")),
                            "map": map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("maxPlayers"),
                            "bots": item.get("bots")})

    subview_header = request.headers.get("x-fetch-subview")
    if subview_header is not None and (subview_header.isnumeric() and int(subview_header) == 1):
        response = make_response(render_template("servers_item.html", server_list=server_list))
    else:
        response = make_response(render_template("servers.html",
                                                 server_list=server_list,
                                                 show_server_list=True))
    response.headers.set("Vary", "x-fetch-subview")
    response.headers.set("Cache-Control", "no-cache, no-store")
    return response

@bp.route("/favorites")
@limiter.limit("90 per minute")
@cache.cached(timeout=5)
def get_favorites():
    """Favorite servers view."""
    return render_template("servers.html", show_server_list=False)

@bp.route("/fetch_favorites_subview", methods=["POST"])
@limiter.limit("90 per minute")
async def get_favorites_subview():
    """Subview for the favorites view for fetching all infomation about favorited servers."""
    request_data = request.get_json()
    servers = request_data.get("servers")
    server_list = []
    async with aiohttp.ClientSession() as session:
        for item in servers:
            item: dict
            server_ip = item.get("server_ip")
            server_port = item.get("server_port")
            fetch_tasks = [asyncio.create_task(steamutils.get_server_info(
                            session, server_ip, server_port))]
            fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        if item is None:
            continue
        server_addr = parse_hostname(item.get("addr"))
        server_tags = tuple(item.get("gametype").split(","))
        vanilla_status = get_vanilla_status_str(server_tags, item)
        server_list.append({"name": item.get("name"),
                            "ip": item.get("addr"),
                            "addr": server_addr[0],
                            "port": server_addr[1],
                            "password": False,
                            "tags": ", ".join(server_tags),
                            "region": get_region_str(item.get("region")),
                            "vanilla": vanilla_status[1],
                            "raw_map": item.get("map"),
                            "game_mode": map_name_to_game_mode(item.get("map")),
                            "map": map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("max_players"),
                            "bots": item.get("bots")})
    response = make_response(render_template("servers_item.html", server_list=server_list))
    response.headers.set("Cache-Control", "no-cache, no-store")
    return response

@bp.route("/server_count")
@limiter.limit("90 per minute")
@cache.cached(timeout=600)
async def get_server_count():
    """Get the amount of active servers."""
    server_count = 0
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(fetch_servers(session, item, False))
                       for item in SERVERBROWSER_TF_GAMEMODES_NO_MVM]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_count += len(item)
    return Response(str(server_count), mimetype="text/plain")

@bp.route("/player_count")
@limiter.limit("90 per minute")
@cache.cached(timeout=300)
async def get_player_count():
    """Get the amount of active players."""
    player_count = 0
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(fetch_servers(session, item, False))
                       for item in SERVERBROWSER_TF_GAMEMODES_NO_MVM]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        for server in item:
            player_count += server.get("players") - server.get("bots")
    return Response(str(player_count), mimetype="text/plain")
