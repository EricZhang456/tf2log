from flask import Blueprint, render_template
from app.extensions import limiter

import asyncio, aiohttp

from app.utils.server_list import ServerList
from app.utils.map_utils import MapUtils

bp = Blueprint("servers", __name__, url_prefix="/servers")

@bp.route("/")
@limiter.limit("90 per minute")
async def get_server_list():
    server_list_raw = []
    server_list = []
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item)) 
                       for item in ServerList.SERVERBROWSER_TF_GAMEMODES]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_list_raw.extend(item)
    for item in server_list_raw:
        server_list.append({"name": item.get("name"), 
                            "ip": item.get("ip"),
                            "vanilla": False if (any(i in item.get("keywords") for i in ServerList.NON_VANILLA_TAGS)
                                                or MapUtils.map_name_to_game_mode(item.get("map")) is None) else True,
                            "game_mode": MapUtils.map_name_to_game_mode(item.get("map")),
                            "map": MapUtils.map_name_to_readable_name(item.get("map")),
                            "players": item.get("players"),
                            "maxPlayers": item.get("maxPlayers"),
                            "bots": item.get("bots")})
    return render_template("servers.html", server_list = server_list, length = len(server_list))
