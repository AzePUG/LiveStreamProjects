from settings.settings import BaseSettings
import os

class DevelopSettings(BaseSettings):
    
    DEBUG=True
    ENV="development"
    SQLALCHEMY_DATABASE_URI = f"postgresql:///testdb"
