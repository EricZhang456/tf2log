from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from geoip2 import database

from .utils.steam_utils import SteamUtils

def page_not_found(_):
    return render_template("except.html", except_body="Page not found."), 404

def internal_server_error(_):
    return render_template("except.html", except_body="Internal server error."), 500

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
limiter = Limiter(
    key_func = get_remote_address,
    default_limits = "120 per minute",
)

class GeoIP:
    def init_app(self, app):
        self.geoip_reader = database.Reader(app.config["GEOLITE2_DB_PATH"])

geoip = GeoIP()

steamutils = SteamUtils()
