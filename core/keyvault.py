import logging
import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_client() -> SecretClient:
    vault_name = os.environ.get("KEY_VAULT_NAME")
    if not vault_name:
        raise EnvironmentError("KEY_VAULT_NAME environment variable is not set.")
    vault_url = f"https://{vault_name}.vault.azure.net"
    logger.info("Initializing Key Vault client for %s", vault_url)
    return SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())


@lru_cache(maxsize=None)
def get_secret(name: str) -> str:
    logger.debug("Fetching secret: %s", name)
    return _get_client().get_secret(name).value
