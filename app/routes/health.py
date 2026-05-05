import logging

from flask import Blueprint, jsonify

from core.db import get_connection

logger = logging.getLogger(__name__)
health_bp = Blueprint("health", __name__)


@health_bp.route("/")
def index():
    return jsonify({
        "status": "ok",
        "service": "SE4453 Azure Hello App",
    })


@health_bp.route("/hello")
def hello():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                pg_version = cur.fetchone()[0]

        logger.info("Database query successful")
        return jsonify({
            "status": "ok",
            "message": "Hello from Azure App Service! FİNAL PROJECT WORKS AS EXPECTED!",
            "database": {
                "connected": True,
                "version": pg_version,
            },
        })

    except EnvironmentError as e:
        logger.error("Configuration error: %s", e)
        return jsonify({
            "status": "error",
            "message": "Service misconfigured.",
            "detail": str(e),
        }), 503

    except Exception as e:
        logger.exception("Database connection failed")
        return jsonify({
            "status": "error",
            "message": "Database connection failed.",
            "detail": str(e),
        }), 500
