from app_init.app_factory import create_app
from flask import jsonify,current_app,request
from app.models import Users,Todo
from app.serializer import UserSchema,UpdateSchema,TodoUpdateSchema,TodoSchema
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,get_jwt_claims,create_refresh_token,jwt_refresh_token_required
from marshmallow import ValidationError
from app.utils import verify_secret
import os
import warnings

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

            return UserSchema(load_only=['password']).jsonify(user)
        except ValidationError as err:
            return jsonify(err.messages)

    return jsonify({'message': "User not found"}),404


@app.route("/api/v1/users",methods=["GET"])
def get_users():
    users = Users.query.all()
    return  UserSchema(load_only=['password']).jsonify(users,many=True)


@app.route("/api/v1/users/<int:id>",methods=["DELETE"])
def delete_user(id):
    user = Users.query.get(id)
    if user.delete():
        return jsonify({"result": True})
    return jsonify({'message': "User not found"}),404



@app.route("/api/v1/users/login",methods=["POST"])
def login_user():
    user_data = request.get_json()
    user = Users.query.filter_by(email=user_data.get("email")).first()

    if not user:
        return jsonify({'message': "User not found"}),404

    if verify_secret(user_data.get("password"),user.password):
        schema = UserSchema()
        user = schema.dump(user)
        access_token = create_access_token(identity=user.get("id"))
        refresh_token = create_refresh_token(identity=user.get("id"))
        user.update(access_token=access_token,refresh_token=refresh_token)
        return jsonify(user)
    return jsonify({'message': "User not found"}),404
    


@app.route("/api/v1/users/todos",methods=["POST"])
@jwt_required
def create_todo():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': "User not found"}),404
    todo_data = request.get_json()
    schema = TodoSchema()
    todo = schema.load(todo_data)
    todo.user_id = user.id
    todo.save_db()
    

    return TodoSchema().jsonify(todo)




@app.route("/api/v1/users/todos",methods=["GET"])
@jwt_required
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id= user_id).all()
    return TodoSchema().jsonify(todos,many=True)


@app.route("/api/v1/users/todos/<todo_id>",methods=["GET"])
@jwt_required
def get_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id = user_id,id = todo_id).first()
    return TodoSchema().jsonify(todos)



@app.route("/api/v1/users/todos/<todo_id>",methods=["PUT"])
@jwt_required
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id = user_id,id = todo_id).first()
    if not todos:
        return jsonify({'message': "Todo not found"}),404
    
    todo = TodoUpdateSchema().load(request.get_json())
    todos.update(**todo)
    return TodoSchema().jsonify(todos)


@app.route("/api/v1/users/todos/<todo_id>",methods=["DELETE"])
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id = user_id,id = todo_id).first()
    user_claims = get_jwt_claims()
   
    if not todos:
        return jsonify({'message': "Todo not found"}),404

    result = todos.delete()
    return jsonify({'message': result})
   



@app.route("/api/v1/users/token/refresh",methods=["POST"])
@jwt_refresh_token_required
def refresh_user_token():
    identity = get_jwt_identity() 
    
    user = Users.query.get(identity)
    if not user:
        return jsonify({"result": "Oops..."}),401

    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)