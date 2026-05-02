import os
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@lru_cache(maxsize=1)
def _get_client() -> SecretClient:
    vault_name = os.environ["KEY_VAULT_NAME"]
    vault_url = f"https://{vault_name}.vault.azure.net"
    return SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())


@lru_cache(maxsize=None)
def get_secret(name: str) -> str:
    return _get_client().get_secret(name).value
