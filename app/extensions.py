from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from geoip2 import database

db = SQLAlchemy()
cache = Cache()

class GeoIP:
    def init_app(self, app):
        self.geoip_reader = database.Reader(app.config["GEOLITE2_DB_PATH"])

geoip = GeoIP()
