import os


class Config:
    TESTING = False
    KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
