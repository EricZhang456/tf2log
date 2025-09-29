"""Info view."""

import socket
import asyncio
from datetime import timedelta

import aiodns
import aiohttp

from quart import Blueprint, Response, current_app, request, render_template, jsonify, abort
from quart_rate_limiter import rate_limit
from a2s import BrokenMessageError, BufferExhaustedError

from tf2log.extensions import cache
from tf2log.utils.server_info_utils import (process_time, format_location, is_ip_fake_ip,
                                            is_port_valid)
from tf2log.utils import format_a2s
from tf2log.utils.cvar_utils import get_next_map, rules_to_readable_dict
from tf2log.utils.map_utils import (map_name_to_game_mode, map_name_to_readable_name,
                                    resolve_workshop_map_name, get_workshop_map_id)
from tf2log.utils.custom_except import NotTF2, ServerSourceTV, BadServerResponse

bp = Blueprint("info", __name__, url_prefix="/info")


@bp.route("/<server_ip>")
@rate_limit(90, timedelta(minutes=1))
@cache.cached(timeout=5, query_string=True)
async def get_info(server_ip: str):
    """Main server info view.

    :param str server_ip: Server IP.
    """
    if is_ip_fake_ip(server_ip):
        return await render_template("except.html", except_body="SDR Fake IP not supported."), 400
    server_port = request.args.get("port", default=27015, type=int)
    if not is_port_valid(server_port):
        return await render_template("except.html", except_body="Invalid port number."), 400

    async with aiodns.DNSResolver() as resolver:
        server_ip_res = await resolver.gethostbyname(server_ip, socket.AddressFamily.AF_INET) # pylint: disable = no-member
    server_ip = server_ip_res.name

    try:
        server_info, server_rules_raw, player_list = await asyncio.gather(
            asyncio.create_task(format_a2s.info(server_ip, server_port)),
            asyncio.create_task(format_a2s.rules(server_ip, server_port)),
            asyncio.create_task(format_a2s.players(server_ip, server_port)),
        )
    except OSError as e:
        if type(e) is OSError: # pylint: disable = unidiomatic-typecheck
            raise BadServerResponse from e
        raise e

    if server_info.get("appid") != 440:
        raise NotTF2
    if server_port == server_info.get("stv_port"):
        raise ServerSourceTV

    server_rules_raw["tf2log_vac"] = 1 if server_info.get("vac") else 0
    server_rules = rules_to_readable_dict(server_rules_raw)
    current_map_raw = server_info.get("map")
    server_tags = ", ".join(server_info.get("tags"))
    next_map_raw = get_next_map(server_rules_raw)
    next_map_workshop_id = None
    if next_map_raw is not None:
        next_map_raw = resolve_workshop_map_name(next_map_raw)
        next_map_workshop_id = get_workshop_map_id(get_next_map(server_rules_raw))
    game_mode = map_name_to_game_mode(current_map_raw)
    current_map = map_name_to_readable_name(current_map_raw)
    next_map = None
    next_map_game_mode = None
    if next_map_raw is not None:
        next_map = map_name_to_readable_name(next_map_raw)
        next_map_game_mode = map_name_to_game_mode(next_map_raw)

    return await render_template("info.html",
                                server_name=server_info.get("name").replace("\x01", ""),
                                player_count=server_info.get("player_count"),
                                max_players=server_info.get("max_players"),
                                raw_map_name=server_info.get("map"),
                                bot_count=server_info.get("bot_count"),
                                password=server_info.get("password"),
                                server_ip=server_ip,
                                server_port=server_port,
                                location=format_location(server_ip),
                                sourcetv_port=server_info.get("stv_port"),
                                player_list=process_time(player_list),
                                server_rules=server_rules,
                                server_tags=server_tags,
                                server_steam_group=server_rules_raw.get("sv_steamgroup"),
                                current_map=current_map,
                                game_mode=game_mode,
                                next_map=next_map,
                                next_map_game_mode=next_map_game_mode,
                                next_map_workshop_id=next_map_workshop_id)


@bp.route("/thumbnail/<map_name>")
@rate_limit(90, timedelta(minutes=1))
@cache.cached(timeout=3600)
async def get_map_thumbnail(map_name: str):
    """Map thumbnail view, fetches a map thumbnail URL from Teamwork.tf.

    :param str map_name: Name of the map.
    """
    teamwork_secret_key = current_app.config.get("TEAMWORK_TF_SECRET_KEY")
    if teamwork_secret_key is None:
        return Response(status=500)
    target_tw_url = f"https://teamwork.tf/api/v1/map-stats/mapthumbnail/{map_name}" + \
                    f"?key={teamwork_secret_key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(target_tw_url, timeout=aiohttp.ClientTimeout(30)) as response:
            response_json = await response.json()
            thumbnail_url = response_json.get("thumbnail")
    if thumbnail_url is not None:
        return Response(thumbnail_url, mimetype="text/plain")
    return Response(status=404)


@bp.route("/sourcetv/<server_ip>")
@rate_limit(90, timedelta(minutes=1))
@cache.cached(timeout=500, query_string=True)
async def get_source_tv(server_ip: str):
    """Check if SourceTV on server is valid.

    :param server_ip: IP of the server with a SourceTV port.
    """
    server_port = request.args.get("port", default=27015, type=int)
    server_info = await format_a2s.info(server_ip, server_port)
    sourcetv_port = server_info.get("stv_port")
    if sourcetv_port != server_port:
        return Response(status=400)
    if sourcetv_port is None:
        return Response(status=404)
    sourcetv_info = await format_a2s.info(server_ip, sourcetv_port)
    if sourcetv_info.get("max_players") == 0:
        return Response(status=404)
    sourcetv_response = {
        "address": f"{server_ip}:{sourcetv_port}",
        "password": sourcetv_info.get("password"),
    }
    return jsonify(sourcetv_response)


@bp.errorhandler(NotTF2)
async def handle_nottf2(_):
    """Not TF2 server error handler."""
    return await render_template("except.html",
                                 except_body="Server is not running TF2."), 404


@bp.errorhandler(ServerSourceTV)
async def handle_server_sourcetv(_):
    """SourceTV relay server error handler."""
    return await render_template("except.html",
                                 except_body="Server is a SourceTV relay."), 400


@bp.errorhandler(TimeoutError)
async def handle_timeout(_):
    """Timeout error handler."""
    return await render_template("except.html",
                                 except_body="Timed out when fetching game server data."), 504


@bp.errorhandler(socket.gaierror)
@bp.errorhandler(aiodns.error.DNSError)
async def handle_invalid_address(_):
    """Invalid server address handler."""
    return await render_template("except.html",
                                 except_body="Invalid server address."), 400


@bp.errorhandler(ConnectionRefusedError)
async def handle_conn_refused(_):
    """Connection refused handler."""
    return await render_template("except.html",
                                 except_body="Cannot connect to game server."), 502


@bp.errorhandler(BrokenMessageError)
@bp.errorhandler(BufferExhaustedError)
@bp.errorhandler(BadServerResponse)
async def handle_broken_message(_):
    """Bad A2S message error handler."""
    return await render_template("except.html",
                                 except_body="Cannot decode response from game server."), 502


@bp.errorhandler(OSError)
async def handle_general_error(_):
    """General error hander."""
    abort(500)
