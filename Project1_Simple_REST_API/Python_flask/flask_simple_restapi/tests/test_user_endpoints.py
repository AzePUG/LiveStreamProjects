from app.models import Users, Todo
from app.serializer import UserSchema, UpdateSchema, TodoSchema, TodoUpdateSchema
from app.utils import verify_secret, get_secret_hash
from app.custom_errors import PasswordLength
import pytest
from http import HTTPStatus
from time import sleep


def test_404_errors(client):
    response = client.get("/")
    assert response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"message": "not found"}

    response = client.get("/unknown")
    assert response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"message": "not found"}

    response = client.post("/test/test")
    assert response.json
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"message": "not found"}


def test_create_user_without_db_init(client):
    url = "/api/v1/users"

    user_data = {
        "first_name": "Test",
        "last_name": "Testing",
        "user_name": "Test_T",
        "email": "test@test.com",
        "password": "Test12345",
    }

    response = client.post(url, json=user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"message": "Sorry, user not created"}


def test_405_error(client):
    url = "/api/v1/users"
    response = client.post(url + "/1")
    assert response.json
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json == {"message": "method not allowed"}

    response = client.patch(url)
    assert response.json
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json == {"message": "method not allowed"}


def test_get_user(client, init_db_users):
    url = "/api/v1/users"
    users = [
        {
            "first_name": "Shehriyar",
            "last_name": "Rzayev",
            "user_name": "shako",
            "email": "test1@mail.ru",
            "password": "Test12345",
        },
        {
            "first_name": "Sebuhi",
            "last_name": "Shukurov",
            "user_name": "sebuhi_sh",
            "email": "test2@mail.ru",
            "password": "Test12345",
        },
    ]
    user_id = 1
    response = client.get(f"{url}/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    user_response = response.json
    assert user_response["id"] == user_id
    assert user_response["todos"] == []

    for key, value in users[0].items():
        if key in user_response.keys():
            if key == "password":
                assert verify_secret(value, user_response[key])
                continue
            assert user_response[key] == value

    user_id = 2
    response = client.get(f"{url}/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    user_response = response.json
    assert user_response["id"] == user_id
    assert user_response["todos"] == []

    for key, value in users[1].items():
        if key in user_response.keys():
            if key == "password":
                assert verify_secret(value, user_response[key])
                continue
            assert user_response[key] == value


def test_user_create(client, init_db_users):
    url = "/api/v1/users"
    user_info = {
        "first_name": "Tural",
        "last_name": "Muradov",
        "user_name": "tural_m",
        "email": "tural@example.ru",
        "password": "Test12345",
    }
    response = client.post(url, json=user_info)
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    user_response = response.json
    for key, value in user_info.items():
        if key in user_response.keys():
            if key == "password":
                assert verify_secret(value, user_response[key])
                continue
            assert user_response[key] == value

    response = client.get(f"{url}/{user_response['id']}")
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json == user_response


def test_user_create_with_invalid_data(client, init_db_users, invalid_data):
    url = "/api/v1/users"
    for i in range(len(invalid_data)):
        response = client.post(url, json=invalid_data[i])
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.is_json


def test_user_update(client, init_db_users):
    url = "/api/v1/users"
    user_id = 1

    response = client.put(f"{url}/{user_id}", json={"first_name": "Tural"})

    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    response = client.get(f"{url}/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json.get("first_name") == "Tural"

    response = client.put(
        f"{url}/{user_id}", json={"first_name": "Shako", "email": "testupdated@mail.ru"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    response = client.get(f"{url}/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert response.json.get("first_name") == "Shako"
    assert response.json.get("email") == "testupdated@mail.ru"

    response = client.put(f"{url}/{user_id}", json={"email2": "testupdated@mail.ru"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.is_json
    assert "email2" in response.json.keys()


def test_get_all_users(client, init_db_users):
    url = "/api/v1/users"
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert len(response.json) == 2


def test_delete_user(client, init_db_users):
    url = "/api/v1/users"
    user_id = 1
    response = client.delete(f"{url}/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"result": True}
    user_id = 30
    response = client.delete(f"{url}/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"message": "User not found"}


def test_login(client, init_db_users):
    url = "/api/v1/users/login"

    response = client.post(
        url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.is_json
    assert "access_token" in response.json.keys()
    assert "refresh_token" in response.json.keys()

    response = client.post(url, json={"email": "te@mail.ru", "password": "Test12345"})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.is_json
    assert response.json == {"message": "User not found"}

    with pytest.raises(PasswordLength):
        response = client.post(url, json={"email": "test1@mail.ru", "password": "'"})

    response = client.post(
        url,
        json={
            "email": "te@mail.ru",
            "password": "2BE85E44E7B610296864814B95AE28C8BACD29488E1772939FCF421614D3B04C",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.is_json
    assert response.json == {"message": "User not found"}

    response = client.post(
        url,
        json={
            "email": "te&mail.ru",
            "password": "2BE85E44E7B610296864814B95AE28C8BACD29488E1772939FCF421614D3B04C",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.is_json
    assert response.json == {"message": "User not found"}


def test_token_expires(client, init_db_users):
    url = "/api/v1/users/login"
    todos_url = "/api/v1/users/todos"

    response = client.post(
        url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    todo_respone = client.get(
        todos_url, headers={"Authorization": f"Bearer {response.json['access_token']}"}
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.OK

    sleep(5)

    todo_respone = client.get(
        todos_url, headers={"Authorization": f"Bearer {response.json['access_token']}"}
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.UNAUTHORIZED
    assert todo_respone.json == {"msg": "Token has expired"}


def test_refresh_token(client, init_db_users):
    url = "/api/v1/users/login"
    todos_url = "/api/v1/users/todos"
    refresh_token_url = "/api/v1/users/token/refresh"
    response = client.post(
        url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    todo_respone = client.get(
        todos_url, headers={"Authorization": f"Bearer {response.json['access_token']}"}
    )

    sleep(5)

    todo_respone = client.get(
        todos_url, headers={"Authorization": f"Bearer {response.json['access_token']}"}
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.UNAUTHORIZED
    assert todo_respone.json == {"msg": "Token has expired"}

    refresh_response = client.post(
        refresh_token_url,
        headers={"Authorization": f"Bearer {response.json['refresh_token']}"},
    )
    assert refresh_response.is_json
    assert refresh_response.status_code == HTTPStatus.OK

    todo_respone = client.get(
        todos_url,
        headers={"Authorization": f"Bearer {refresh_response.json['access_token']}"},
    )

    assert todo_respone.is_json
    assert todo_respone.status_code == HTTPStatus.OK

    response = client.post(
        url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    refresh_response = client.post(
        refresh_token_url,
        headers={"Authorization": f"Bearer {response.json['access_token']}"},
    )

    assert refresh_response.is_json
    assert refresh_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert refresh_response.json == {"msg": "Only refresh tokens are allowed"}


def test_refresh_token_expire(client, init_db_users):
    url = "/api/v1/users/login"
    todos_url = "/api/v1/users/todos"
    refresh_token_url = "/api/v1/users/token/refresh"

    response = client.post(
        url, json={"email": "test1@mail.ru", "password": "Test12345"}
    )

    todo_respone = client.get(
        todos_url, headers={"Authorization": f"Bearer {response.json['access_token']}"}
    )
    assert todo_respone.status_code == HTTPStatus.OK

    sleep(6)

    refresh_response = client.post(
        refresh_token_url,
        headers={"Authorization": f"Bearer {response.json['refresh_token']}"},
    )

    assert refresh_response.is_json
    assert refresh_response.status_code == HTTPStatus.UNAUTHORIZED
    assert refresh_response.json == {"msg": "Token has expired"}
