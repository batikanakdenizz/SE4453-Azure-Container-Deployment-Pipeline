from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

app = Flask(__name__)


def get_required_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing environment variable: {name}")
    return value


def get_db_connection():
    return psycopg2.connect(
        host=get_required_env("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        database=get_required_env("DB_NAME"),
        user=get_required_env("DB_USER"),
        password=get_required_env("DB_PASSWORD"),
    )


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint. Returns backend status."""
    return (
        jsonify({"success": True, "endpoint": "/", "message": "Backend is running"}),
        200,
    )


@app.route("/hello", methods=["GET"])
def hello():
    """Database connectivity test. Queries current server time from PostgreSQL."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()

        return (
            jsonify(
                {
                    "success": True,
                    "endpoint": "/hello",
                    "message": "Hello from Flask!",
                    "database_status": "connected",
                    "server_time": str(result[0]),
                }
            ),
            200,
        )

    except ValueError as e:
        return (
            jsonify(
                {
                    "success": False,
                    "endpoint": "/hello",
                    "message": "Configuration error",
                    "database_status": "not tested",
                    "error": str(e),
                }
            ),
            500,
        )

    except Exception:
        return (
            jsonify(
                {
                    "success": False,
                    "endpoint": "/hello",
                    "message": "Hello from Flask!",
                    "database_status": "connection failed",
                    "error": "Unable to connect to PostgreSQL with the current configuration.",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
