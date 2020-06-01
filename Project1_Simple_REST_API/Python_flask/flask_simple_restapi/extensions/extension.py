from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import validate,fields,validates_schema
from flask_migrate import Migrate
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager

pwd_context = CryptContext(schemes="sha256_crypt")
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()

Model,Column,String,Integer,DateTime,ForeignKey,relationship = db.Model,db.Column,db.String,db.Integer,db.DateTime,db.ForeignKey,db.relationship