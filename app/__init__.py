import os
import json

from flask import Flask

from .extensions import db, migrate, cache, geoip, limiter, steamutils, page_not_found, internal_server_error
from .routes import info
from .models.server import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_file("config.json", json.load)

    # only build css on each request when in debug
    if app.debug or app.config["ENV"] == "dev":
        from sassutils.wsgi import SassMiddleware
        app.wsgi_app = SassMiddleware(app.wsgi_app, {
            "app": {
                "sass_path": "static/sass",
                "css_path": "static/css",
                "wsgi_path": "/static/css",
                "strip_extension": False,
            }
        })

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    for _, _, files in os.walk(app.instance_path):
        if "GeoLite2-City.mmdb" not in files:
            raise Exception("Cannot find GeoLite2 City database")
        else:
            app.config.update(GEOLITE2_DB_PATH=os.path.join(app.instance_path, "GeoLite2-City.mmdb"))
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    geoip.init_app(app)
    limiter.init_app(app)

    steamutils.init_app(app)

    app.register_blueprint(info.bp)

    return app
