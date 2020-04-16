from app_init.app_factory import create_app
from flask import jsonify,current_app,request
import os
import warnings

warnings.simplefilter("ignore")

settings_name = os.getenv("settings")

app =create_app(settings_name)
users = []
Id = 0

@app.route("/api/v1/users",methods=["POST"])
def create_user():
    global Id
    user_info = request.get_json()
    user_info["Id"] = Id
    Id += 1
    users.append(user_info)
    return jsonify(user_info)


@app.route("/api/v1/users/<int:id>",methods=["GET"])
def get_user(id):
    for i in users:
        if i.get("Id") == id:
            return jsonify(i)
    
    return jsonify({'message': "User not found"}),404
    

@app.route("/api/v1/users/<int:id>",methods=["PUT"])
def update_user(id):
    user_info = request.json
    for index,value in enumerate(users):
        if value.get("Id") == id:
            value.update(user_info)
            users[index] = value        

            current_app.logger.info("User info updated")
            return jsonify(user_info)
    return jsonify({'message': "User not found"}),404


@app.route("/api/v1/users",methods=["GET"])
def get_users():
    return jsonify(users)



@app.route("/api/v1/users/<int:id>",methods=["DELETE"])
def delete_user(id):

    for index,value in enumerate(users):
        if value.get("Id") == id:
            del users[index]

            current_app.logger.info("User deleted")
            return jsonify({"result": True})

    return jsonify({'message': "User not found"}),404