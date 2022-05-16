from flask import Flask

from src.entrypoints.api.rest import convert


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    config_module = f"src.entrypoints.api.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(convert.blueprint)
    return app
