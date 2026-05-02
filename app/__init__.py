import logging

from flask import Flask

from app.config import config as app_config
from app.routes import register_routes


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)

    cfg = app_config[config_name]
    app.config.from_object(cfg)

    _configure_logging(app)
    register_routes(app)

    try:
        cfg.validate()
    except EnvironmentError as e:
        app.logger.warning("Startup validation warning: %s", e)

    return app


def _configure_logging(app: Flask) -> None:
    log_level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
