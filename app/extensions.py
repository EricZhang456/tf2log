from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from geoip2 import database

db = SQLAlchemy()
cache = Cache()
limiter = Limiter(get_remote_address)

class GeoIP:
    def init_app(self, app):
        self.geoip_reader = database.Reader(app.config["GEOLITE2_DB_PATH"])

geoip = GeoIP()
