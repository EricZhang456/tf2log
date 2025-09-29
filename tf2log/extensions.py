"""Application extensions."""

# pylint: disable = too-few-public-methods

from quart import render_template, Quart
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from geoip2 import database

from .utils.steam_utils import SteamUtils


async def page_not_found(_):
    """Custom 404 page."""
    return await render_template("except.html", except_body="Page not found.",
                                                except_title="Page Not Found"), 404


async def internal_server_error(_):
    """Custom 500 page."""
    return await render_template("except.html", except_body="Internal server error.",
                                                except_title="Internal Server Error"), 500


cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120 per minute"],
)


class GeoIP:
    """GeoIP reader class."""
    def __init__(self):
        self.geoip_reader = None

    def init_app(self, app: Quart):
        """Initialize the GeoIP reader.

        :param Quart app: A Quart object with the GEOLITE2_DB_PATH config pointing
                          to a GeoLite2 database.
        """
        self.geoip_reader = database.Reader(app.config["GEOLITE2_DB_PATH"])


geoip = GeoIP()
steamutils = SteamUtils()
