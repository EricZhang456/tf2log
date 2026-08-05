"""Server list view"""

import asyncio
from datetime import timedelta

import aiohttp

from quart import Blueprint, render_template, request, make_response
from quart_rate_limiter import rate_limit

from tf2log.extensions import steamutils
from tf2log.utils.game_presets import GamePresets
from tf2log.utils.parse_hostname import parse_hostname
from tf2log.utils.param_bool import param_bool
from tf2log.utils.server_list import get_region_str, ServerRegions
from tf2log.utils.map_utils import map_name_to_game_mode, map_name_to_readable_name
from tf2log.utils.server_list import get_vanilla_status_str

bp = Blueprint("servers", __name__, url_prefix="/servers")

QUERY_PARAMS = ("alltalk", "nocrits", "gravity", "increased_maxplayers", "respawntimes",
                "friendlyfire", "dmgspread", "norespawntime", "replays", "highlander")

ILLEGAL_VANILLA_PARAMS = ("nocrits", "gravity", "dmgspread", "respawntimes", "norespawntimes",
                          "highlander", "trade", "friendlyfire")

@bp.route("/")
@rate_limit(90, timedelta(minutes=1))
async def get_server_list():
    """Main server list view."""
    has_user_playing = request.args.get("has_user_playing", default=True, type=param_bool)
    not_full = request.args.get("not_full", default=False, type=param_bool)
    # no_password = request.args.get("password", default=False, type=param_bool)

    region_param = request.args.get("region", default=-1, type=int)
    region = ServerRegions(region_param) if region_param != -1 else None
    vanilla = GamePresets(request.args.get("vanilla", default=1, type=int))

    query_params = []
    server_list = []
    additional_nors = []
    if has_user_playing:
        query_params.append("\\empty\\1")
    if not_full:
        query_params.append("\\full\\1")
    if region and region != ServerRegions.WORLD:
        query_params.append(f"\\region\\{region.value}")
    target_params = []
    for param in QUERY_PARAMS:
        if request.args.get(param, default=False, type=param_bool) and not (
            vanilla == GamePresets.VANILLA and param in ILLEGAL_VANILLA_PARAMS):
            target_params.append(param)
    if target_params:
        query_params.append(f"\\gametype\\{",".join(target_params)}")

    if vanilla == GamePresets.VANILLA:
        for i in ILLEGAL_VANILLA_PARAMS:
            additional_nors.append(f"\\gametype\\{i}")

    # doesn't seem to work with the steam backend
    # if no_password:
    #     query_params.append("\\password\\0")

    async with aiohttp.ClientSession() as session:
        server_list_raw = await steamutils.fetch_servers(session, query_params, additional_nors)

    for item in server_list_raw:
        item: dict
        # sometimes a sdr server won't have a map
        server_map = item.get("map")
        if not server_map:
            continue
        server_map = server_map.strip().lower()
        if not server_map:
            continue
        if server_map == "nothing":
            continue
        server_gametype = item.get("gametype")
        if server_gametype is None:
            server_gametype = ""
        server_tags = server_gametype.split(",")
        server_addr = parse_hostname(item.get("addr"))
        server_qualified = True
        server_region = item.get("region")
        if region == ServerRegions.WORLD and ServerRegions(server_region) != ServerRegions.WORLD:
            continue
        for param in QUERY_PARAMS:
            if request.args.get(param, default=False, type=param_bool) and param not in server_tags:
                server_qualified = False
                break
        if not server_qualified:
            continue

        vanilla_status = get_vanilla_status_str(server_tags, item)
        # if requested preset is not all and is not the preset selected
        if vanilla not in {vanilla_status[0], GamePresets.ALL}:
            continue

        server_list.append({"name": item.get("name"),
                            "ip": item.get("addr"),
                            "addr": server_addr[0],
                            "port": server_addr[1],
                            "tags": ", ".join(server_tags),
                            "region": get_region_str(server_region),
                            "vanilla": vanilla_status[1],
                            "raw_map": item.get("map"),
                            "game_mode": map_name_to_game_mode(server_map),
                            "map": map_name_to_readable_name(server_map),
                            "players": item.get("players"),
                            "maxPlayers": item.get("max_players"),
                            "bots": item.get("bots")})

    subview_header = request.headers.get("x-fetch-subview")
    if subview_header is not None and (subview_header.isnumeric() and int(subview_header) == 1):
        response = await make_response(await render_template("servers_item.html", server_list=server_list))
    else:
        response = await make_response(await render_template("servers.html",
                                                       server_list=server_list,
                                                       show_server_list=True))
    response.headers.set("Vary", "x-fetch-subview")
    response.headers.set("Cache-Control", "no-cache, no-store")
    return response


@bp.route("/favorites")
@rate_limit(90, timedelta(minutes=1))
async def get_favorites():
    """Favorite servers view."""
    return await render_template("servers.html", show_server_list=False)


@bp.route("/fetch_favorites_subview", methods=["POST"])
@rate_limit(90, timedelta(minutes=1))
async def get_favorites_subview():
    """Subview for the favorites view for fetching all infomation about favorited servers."""
    req_data = await request.get_json()
    servers = req_data.get("servers")
    if not servers:
        return ""
    server_list = []
    fetch_tasks = []
    async with aiohttp.ClientSession() as session:
        for item in servers:
            item: dict
            fetch_tasks.append(
                asyncio.create_task(steamutils.get_server_info(session,
                                                               item.get("server_ip"),
                                                               item.get("server_port"))))
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        if not item:
            continue
        server_addr = parse_hostname(item.get("addr"))
        server_tags = item.get("gametype").split(",")
        vanilla_status = get_vanilla_status_str(server_tags, item)
        server_list.append({"name": item.get("name"),
                            "ip": item.get("addr"),
                            "addr": server_addr[0],
                            "port": server_addr[1],
                            "tags": ", ".join(server_tags),
                            "region": get_region_str(item.get("region")),
                            "vanilla": vanilla_status[1],
                            "raw_map": item.get("map"),
                            "game_mode": map_name_to_game_mode(item.get("map")),
                            "map": map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("max_players"),
                            "bots": item.get("bots")})
    response = await make_response(await render_template("servers_item.html", server_list=server_list))
    response.headers.set("Cache-Control", "no-cache, no-store")
    return response


@bp.route("/server_count")
@rate_limit(90, timedelta(minutes=1))
async def get_server_count():
    """Get the amount of active servers."""
    async with aiohttp.ClientSession() as session:
        fetch_result = await steamutils.fetch_servers(session)
    response = await make_response(str(len(fetch_result)))
    response.mimetype = "text/plain"
    return response


@bp.route("/player_count")
@rate_limit(90, timedelta(minutes=1))
async def get_player_count():
    """Get the amount of active players."""
    player_count = 0
    async with aiohttp.ClientSession() as session:
        fetch_result = await steamutils.fetch_servers(session, ("\\empty\\1"))
    for server in fetch_result:
        player_count += server.get("players") - server.get("bots")
    response = await make_response(str(player_count))
    response.mimetype = "text/plain"
    return response
