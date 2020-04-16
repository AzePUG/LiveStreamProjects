from flask_env import MetaFlaskEnv
import os

project_name = "flask_template"


class BaseSettings(metaclass=MetaFlaskEnv):

    DEBUG = True

    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "app.%s.log" % project_name