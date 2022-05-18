import os
from src.entrypoints.api.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
