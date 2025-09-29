"""Index view."""

from quart import Blueprint, redirect, url_for

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/")
async def get_index():
    """Redirects to server list when fetching index."""
    return redirect(url_for("servers.get_server_list"))
