from app_init.app_factory import create_app
from flask import jsonify,current_app,request
from app.models import Users
from app.serializer import UserSchema,UpdateSchema,UsersSchema
import os
import warnings
from marshmallow import ValidationError

warnings.simplefilter("ignore")

settings_name = os.getenv("settings")

app = create_app(settings_name)

@app.route("/api/v1/users",methods=["POST"])
def create_user():
    user_info = request.get_json()  
    schema = UserSchema()
    try:
        user = schema.load(user_info)
        user.save_db()

    except ValidationError as err:
        return jsonify(err.messages)

    return UserSchema().jsonify(user)


@app.route("/api/v1/users/<int:id>",methods=["GET"])
def get_user(id):
    user = Users.query.filter_by(id=id).first()
    if user:
        return UserSchema().jsonify(user)
    
    return jsonify({'message': "User not found"}),404
    

@app.route("/api/v1/users/<int:id>",methods=["PUT"])
def update_user(id):
    user_info = request.json
    user = Users.query.get(id)
    if user:
        try:
            schema = UpdateSchema()
            user_info = schema.load(user_info)
            user = user.update(**user_info)
            return UserSchema().jsonify(user)
        except ValidationError as err:
            return jsonify(err.messages)

    return jsonify({'message': "User not found"}),404


@app.route("/api/v1/users",methods=["GET"])
def get_users():
    users = Users.query.all()
    return  UserSchema().jsonify(users,many=True)


@app.route("/api/v1/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    user = Users.query.get(id)
    if user.delete():
        return jsonify({"result": True})
    return jsonify({'message': "User not found"}),404