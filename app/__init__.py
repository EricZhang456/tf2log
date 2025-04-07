import os
import json

from flask import Flask

from .extensions import db, cache
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

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(info.bp)

    return app
