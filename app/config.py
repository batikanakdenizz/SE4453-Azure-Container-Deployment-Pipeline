import os


class Config:
    TESTING = False
    KEY_VAULT_NAME: str = os.environ.get("KEY_VAULT_NAME", "")

    @classmethod
    def validate(cls) -> None:
        if not cls.KEY_VAULT_NAME:
            raise EnvironmentError("KEY_VAULT_NAME environment variable is not set.")


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def validate(cls) -> None:
        pass


class DevelopmentConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
