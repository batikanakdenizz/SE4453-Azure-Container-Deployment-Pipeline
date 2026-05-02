from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/hello")
def hello():
    return jsonify({"message": "Hello from Azure App Service!"})
