import os
import json

from flask import Flask

from .extensions import cache, geoip, limiter, steamutils, page_not_found, internal_server_error
from .routes import info, servers, index

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_file("config.json", json.load)

    if app.config.get("ENV") not in ("dev", "prod"):
        raise Exception("Invalid ENV")

    if app.debug or app.config["ENV"] == "dev":
        from sassutils.wsgi import SassMiddleware
        app.wsgi_app = SassMiddleware(app.wsgi_app, {
            "tf2log": {
                "sass_path": "static/sass",
                "css_path": "static/css",
                "wsgi_path": "/static/css",
                "strip_extension": False,
            }
        })
    else:
        import sass
        if not os.path.exists("tf2log/static/css"):
            os.makedirs("tf2log/static/css")
        with open("tf2log/static/css/style.scss.css", "w") as f:
            f.write(sass.compile(filename="tf2log/static/sass/style.scss", output_style="compressed"))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    if app.config.get("GEOLITE2_DB_PATH") is None:
        for _, _, files in os.walk(app.instance_path):
            if "GeoLite2-City.mmdb" not in files:
                raise Exception("Cannot find GeoLite2 City database")
            else:
                app.config.update(GEOLITE2_DB_PATH=os.path.join(app.instance_path, "GeoLite2-City.mmdb"))
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    cache.init_app(app)
    geoip.init_app(app)
    limiter.init_app(app)

    steamutils.init_app(app)

    app.register_blueprint(info.bp)
    app.register_blueprint(servers.bp)
    app.register_blueprint(index.bp)

    return app
