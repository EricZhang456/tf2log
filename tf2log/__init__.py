"""Application entry point."""

# pylint: disable = import-outside-toplevel

import os
import json

import quart_flask_patch
from quart import Quart

from .extensions import (cache, geoip, limiter, steamutils,
                         page_not_found, internal_server_error)
from .routes import info, servers, index


def create_app():
    """Creates the Quart application."""
    app = Quart(__name__, instance_relative_config=True)

    app.config.from_file("config.json", json.load)

    if app.config.get("ENV") not in {"dev", "prod"}:
        raise ValueError("Invalid ENV")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config.get("GEOLITE2_DB_PATH") is None:
        for _, _, files in os.walk(app.instance_path):
            if "GeoLite2-City.mmdb" not in files:
                raise RuntimeError("Cannot find GeoLite2 City database")
            app.config.update(GEOLITE2_DB_PATH=os.path.join(app.instance_path,
                                                            "GeoLite2-City.mmdb"))

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
