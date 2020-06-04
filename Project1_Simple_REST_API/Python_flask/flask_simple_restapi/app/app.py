from app_init.app_factory import create_app
from flask import jsonify, current_app, request
from app.models import Users, Todo
from app.serializer import UserSchema, UpdateSchema, TodoUpdateSchema, TodoSchema
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt_claims,
    create_refresh_token,
    jwt_refresh_token_required,
)
from marshmallow import ValidationError
from app.utils import verify_secret
from http import HTTPStatus
import os
import warnings

warnings.simplefilter("ignore")

settings_name = os.getenv("settings")

app = create_app(settings_name)


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    user_info = request.get_json()
    schema = UserSchema()
    try:
        user = schema.load(user_info)
        user = user.save_db()
        if not user:
            return jsonify(message="Sorry, user not created"), HTTPStatus.BAD_REQUEST

    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    return UserSchema().jsonify(user)


@app.route("/api/v1/users/<int:id>", methods=["GET"])
def get_user(id):
    user = Users.query.filter_by(id=id).first()
    if user:
        return UserSchema().jsonify(user)

    return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@app.route("/api/v1/users/<int:id>", methods=["PUT"])
def update_user(id):
    user_info = request.json
    user = Users.query.get(id)
    if user:
        try:
            schema = UpdateSchema()
            user_info = schema.load(user_info)
            user = user.update(**user_info)
            if not user:
                return (
                    jsonify(message="Sorry, user data not updated"),
                    HTTPStatus.BAD_REQUEST,
                )
            return UserSchema(load_only=["password"]).jsonify(user)
        except ValidationError as err:
            return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@app.route("/api/v1/users", methods=["GET"])
def get_users():
    users = Users.query.all()
    return UserSchema(load_only=["password"]).jsonify(users, many=True)


@app.route("/api/v1/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = Users.query.get(id)
    if user:
        if user.delete():
            return jsonify({"result": True})
    return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@app.route("/api/v1/users/login", methods=["POST"])
def login_user():
    user_data = request.get_json()
    user = Users.query.filter_by(email=user_data.get("email")).first()

    if not user:
        return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

    if verify_secret(user_data.get("password"), user.password):
        schema = UserSchema()
        user = schema.dump(user)
        access_token = create_access_token(identity=user.get("id"))
        refresh_token = create_refresh_token(identity=user.get("id"))
        user.update(access_token=access_token, refresh_token=refresh_token)
        return jsonify(user)
    return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND


@app.route("/api/v1/users/todos", methods=["POST"])
@jwt_required
def create_todo():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND
    todo_data = request.get_json()
    schema = TodoSchema()
    todo = schema.load(todo_data)
    todo.user_id = user.id
    todo.save_db()

    return TodoSchema().jsonify(todo)


@app.route("/api/v1/users/todos", methods=["GET"])
@jwt_required
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return TodoSchema().jsonify(todos, many=True)


@app.route("/api/v1/users/todos/<todo_id>", methods=["GET"])
@jwt_required
def get_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id, id=todo_id).first()
    if not todos:
        return jsonify(result=False), HTTPStatus.NOT_FOUND
    return TodoSchema().jsonify(todos)


@app.route("/api/v1/users/todos/<todo_id>", methods=["PUT"])
@jwt_required
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id, id=todo_id).first()
    if not todos:
        return jsonify({"message": "Todo not found"}), HTTPStatus.NOT_FOUND

    todo = TodoUpdateSchema().load(request.get_json())
    todos.update(**todo)
    return TodoSchema().jsonify(todos)


@app.route("/api/v1/users/todos/<todo_id>", methods=["DELETE"])
@jwt_required
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id, id=todo_id).first()

    if not todos:
        return jsonify({"message": "Todo not found"}), HTTPStatus.NOT_FOUND

    result = todos.delete()
    return jsonify({"message": result})


@app.route("/api/v1/users/token/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh_user_token():
    identity = get_jwt_identity()

    user = Users.query.get(identity)
    if not user:
        return jsonify({"result": "Oops..."}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@app.errorhandler(HTTPStatus.NOT_FOUND)
def handle_404(e):
    return jsonify(message="not found"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def handle_405(e):
    return jsonify(message="method not allowed"), HTTPStatus.METHOD_NOT_ALLOWED


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify(message="Service unreachable"), HTTPStatus.INTERNAL_SERVER_ERROR
