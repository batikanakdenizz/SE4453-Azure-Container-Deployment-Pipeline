import logging

import psycopg

from core.keyvault import get_secret

logger = logging.getLogger(__name__)


def get_connection() -> psycopg.Connection:
    logger.debug("Opening database connection")
    return psycopg.connect(
        host=get_secret("db-host"),
        dbname=get_secret("db-name"),
        user=get_secret("db-user"),
        password=get_secret("db-password"),
        port=5432,
        sslmode="require",
        connect_timeout=10,
    )
