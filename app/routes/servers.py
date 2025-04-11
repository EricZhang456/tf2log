from flask import Blueprint, render_template
from app.extensions import limiter

import asyncio, aiohttp

from app.utils.server_list import ServerList

bp = Blueprint("servers", __name__, url_prefix="/servers")

@bp.route("/")
@limiter.limit("90 per minute")
async def get_server_list():
    server_list = []
    async with aiohttp.ClientSession() as session:
        fetch_tasks = [asyncio.create_task(ServerList.fetch_servers(session, item)) 
                       for item in ServerList.SERVERBROWSER_TF_GAMEMODES]
        fetch_result = await asyncio.gather(*fetch_tasks)
    for item in fetch_result:
        server_list.extend(item)
    return render_template("servers.html", server_list = server_list, length = len(server_list))
