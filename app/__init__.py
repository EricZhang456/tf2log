import os
import json

from flask import Flask

from .extensions import db, cache, geoip
from .routes import info

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # only build css on each request when in debug
    if app.debug:
        from sassutils.wsgi import SassMiddleware
        app.wsgi_app = SassMiddleware(app.wsgi_app, {
            "app": {
                "sass_path": "static/sass",
                "css_path": "static/css",
                "wsgi_path": "/static/css",
                "strip_extension": False,
            }
        })

    app.config.from_file("config.json", json.load)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    for _, _, files in os.walk(app.instance_path):
        if "GeoLite2-City.mmdb" not in files:
            raise Exception("Cannot find GeoLite2 City database")
        else:
            app.config.update(GEOLITE2_DB_PATH=os.path.join(app.instance_path, "GeoLite2-City.mmdb"))
    
    db.init_app(app)
    cache.init_app(app)
    geoip.init_app(app)

    app.register_blueprint(info.bp)

    return app
