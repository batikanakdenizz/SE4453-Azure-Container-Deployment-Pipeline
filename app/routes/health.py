from flask import Blueprint, jsonify

from core.db import get_connection

health_bp = Blueprint("health", __name__)


@health_bp.route("/hello")
def hello():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
    return jsonify({
        "message": "Hello from Azure App Service!",
        "postgres_version": version,
    })
