from flask import Blueprint, render_template, request, Response
from app.extensions import limiter, cache

import asyncio, aiohttp

from app.utils.server_list import ServerList
from app.utils.map_utils import MapUtils

bp = Blueprint("servers", __name__, url_prefix="/servers")

@bp.route("/")
@limiter.limit("90 per minute")
@cache.cached(timeout=5, query_string=True)
async def get_server_list():
    has_user_playing = request.args.get("has_user_playing", default=False, type=bool)
    vanilla = request.args.get("vanilla", default=True, type=bool)
    alltalk = request.args.get("alltalk", default=False, type=bool)
    nocrits = request.args.get("nocrits", default=False, type=bool)
    gravity = request.args.get("gravity", default=False, type=bool)
    increased_maxplayers = request.args.get("increased_maxplayers", default=False, type=bool)
    respawntimes = request.args.get("respawntimes", default=False, type=bool)
    friendlyfire = request.args.get("friendlyfire", default=False, type=bool)
    dmgspread = request.args.get("dmgspread", default=False, type=bool)
    norespawntime = request.args.get("norespawntime", default=False, type=bool)
    replay = request.args.get("replay", default=False, type=bool)
    server_list_raw = []
    server_list = []
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item, has_user_playing)) 
                       for item in (ServerList.SERVERBROWSER_TF_GAMEMODES_VANILLA 
                                    if vanilla else ServerList.SERVERBROWSER_TF_GAMEMODES_NO_MVM)]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_list_raw.extend(item)
    for item in server_list_raw:
        server_tags = tuple(item.get("keywords").split(","))
        if ((alltalk and "alltalk" not in server_tags)
            or (nocrits and "nocrits" not in server_tags)
            or (gravity and "gravity" not in server_tags)
            or (increased_maxplayers and "increased_maxplayers" not in server_tags)
            or (norespawntime and "norespawntime" not in server_tags)
            or (respawntimes and "respawntimes" not in server_tags)
            or (dmgspread and "dmgspread" not in server_tags)
            or (friendlyfire and "friendlyfire" not in server_tags)
            or (replay and "replays" not in server_tags)):
            continue
        server_list.append({"name": item.get("name"), 
                            "ip": item.get("ip"),
                            "tags": ", ".join(server_tags),
                            "vanilla": False if (any(i in item.get("keywords") for i in ServerList.NON_VANILLA_TAGS)
                                                or MapUtils.map_name_to_game_mode(item.get("map")) is None) else True,
                            "game_mode": MapUtils.map_name_to_game_mode(item.get("map")),
                            "map": MapUtils.map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("maxPlayers"),
                            "bots": item.get("bots")})
    return render_template("servers.html", server_list = server_list, length = len(server_list))

@bp.route("/server_count")
@limiter.limit("90 per minute")
@cache.cached(timeout=600)
async def get_sever_count():
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