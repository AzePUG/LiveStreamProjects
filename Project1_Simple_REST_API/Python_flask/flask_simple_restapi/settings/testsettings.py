from settings.settings import BaseSettings
from datetime import timedelta
import os


class TestSettings(BaseSettings):

    TESTING = True
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = f"postgresql:///testdb"
    JWT_SECRET_KEY = os.urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=5)
