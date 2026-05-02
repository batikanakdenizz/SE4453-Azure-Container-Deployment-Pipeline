from flask import Flask

from app.config import config as app_config
from app.routes import register_routes


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    register_routes(app)
    return app
