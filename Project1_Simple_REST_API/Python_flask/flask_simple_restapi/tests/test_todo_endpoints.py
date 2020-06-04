from app.models import Users, Todo
from app.serializer import UserSchema, UpdateSchema, TodoSchema, TodoUpdateSchema
from app.utils import verify_secret, get_secret_hash
from app.custom_errors import PasswordLength
import pytest
from http import HTTPStatus
from time import sleep


def test_create_todo(client, init_db_users):
    todo_url = "/api/v1/users/todos"
    login_url = "/api/v1/users/login"

    response = client.post(
        login_url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    assert response.status_code == HTTPStatus.OK
    todo_data = {
        "title": "Python",
        "description": "Learn Python with TechAcademy",
        "user_id": response.json["id"],
    }
    todo_respone = client.post(
        todo_url,
        json=todo_data,
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.OK

    for key, val in todo_data.items():
        assert todo_respone.json.get(key) == val

    user = Users.query.get(response.json["id"])

    assert len(user.todos) == 1
    assert user.todos[0].id == todo_respone.json.get("id")

    todo_data = {"title": "Python", "description": "Learn Python with TechAcademy"}

    todo_respone = client.post(todo_url, json=todo_data,)

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.UNAUTHORIZED

    # invalid token
    todo_respone = client.post(
        todo_url,
        json=todo_data,
        headers={
            "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        },
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert todo_respone.json == {"msg": "Signature verification failed"}


def test_get_todo(client, init_db_todos):
    todo_url = "/api/v1/users/todos"
    login_url = "/api/v1/users/login"

    response = client.post(
        login_url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    assert response.status_code == HTTPStatus.OK

    todo_respone = client.get(
        todo_url, headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.OK
    assert isinstance(todo_respone.json, list)
    assert len(todo_respone.json) == 1

    todo_respone = client.get(
        todo_url + "/1",
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.OK

    todo_respone = client.get(
        todo_url + "/10",
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.NOT_FOUND


def test_update_todo(client, init_db_todos):
    todo_url = "/api/v1/users/todos"
    login_url = "/api/v1/users/login"

    response = client.post(
        login_url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    assert response.status_code == HTTPStatus.OK

    todo_respone = client.put(
        todo_url + "/1",
        json={"title": "Python3"},
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.status_code == HTTPStatus.OK
    assert todo_respone.is_json
    assert todo_respone.json["title"] == "Python3"

    todo_respone = client.put(
        todo_url + "/1",
        json={"title": "Python", "description": "Learn Python"},
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.status_code == HTTPStatus.OK
    assert todo_respone.is_json
    assert todo_respone.json["title"] == "Python"
    assert todo_respone.json["description"] == "Learn Python"


def test_delete_todo(client, init_db_todos):
    todo_url = "/api/v1/users/todos"
    login_url = "/api/v1/users/login"

    response = client.post(
        login_url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    assert response.status_code == HTTPStatus.OK

    todo_respone = client.delete(
        todo_url + "/1",
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert todo_respone.status_code == HTTPStatus.OK
    assert todo_respone.is_json

    todo_respone = client.delete(
        todo_url + "/1",
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )
    assert todo_respone.status_code == HTTPStatus.NOT_FOUND
