class Config:
    TESTING = False


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
