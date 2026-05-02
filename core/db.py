import psycopg2

from core.keyvault import get_secret


def get_connection():
    return psycopg2.connect(
        host=get_secret("db-host"),
        dbname=get_secret("db-name"),
        user=get_secret("db-user"),
        password=get_secret("db-password"),
        port=5432,
        sslmode="require",
    )
