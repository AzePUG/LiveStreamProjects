from flask_env import MetaFlaskEnv
import os


class BaseSettings(metaclass=MetaFlaskEnv):
    
    DEBUG = True

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False