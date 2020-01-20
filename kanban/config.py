import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hard to guess string")
    PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TASK_PER_PAGE = 20

    @classmethod
    def init_app(cls, app):
        pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///{0}/db/data-dev.sqlite".format(Config.PROJECT_DIR))


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///{0}/db/data-test.sqlite".format(Config.PROJECT_DIR))


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL", "sqlite:///{0}/db/data-prod.sqlite".format(Config.PROJECT_DIR))

    @classmethod
    def init_app(cls, app):
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {
    "default": DevConfig,
    "dev": DevConfig,
    "test": TestConfig,
    "prod": ProdConfig
}
