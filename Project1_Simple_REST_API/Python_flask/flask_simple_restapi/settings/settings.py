from flask_env import MetaFlaskEnv
import os


class BaseSettings(metaclass=MetaFlaskEnv):

    SECRET_KEY = os.urandom(32)
