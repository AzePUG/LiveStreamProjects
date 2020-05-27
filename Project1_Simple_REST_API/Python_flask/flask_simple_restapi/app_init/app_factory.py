from flask import Flask
import os, logging,sys
from extensions.extension import db,ma,migrate,jwt
from logging.config import dictConfig


settings = {
    "dev" : "settings.devsettings.DevelopSettings",
    "prod" : "settings.prodsettings.ProdSettings"
}

dictConfig({
    'version': 1,
    'formatters': {'default': {
        "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s: %(message)s",
            "datefmt": "%d/%b/%Y:%H:%M:%S",
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

def get_settings(settings_name):
    if settings.get(settings_name):
        return settings.get(settings_name)
    
    raise Exception("Gosterdiyiniz  %s parametr movcud deil" % settings_name)

def create_app(settings_name):
    app = Flask(__name__)
    settings_obj = get_settings(settings_name)
    app.config.from_object(settings_obj)
    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    return app