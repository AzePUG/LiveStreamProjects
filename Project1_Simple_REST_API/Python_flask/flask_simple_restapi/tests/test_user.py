from app.serializer import UserSchema, UpdateSchema
from app.utils import verify_secret, get_secret_hash
from app.models import Users
from app.custom_errors import PasswordLength
from sqlalchemy.exc import IntegrityError
import pytest


def test_user_class(new_user):
    user, user_info = new_user
    for key, val in user_info.items():
        res = getattr(user, key)
        assert res == val


def test_create_user(app, new_user, init_db_users):
    user, user_info = new_user
    with app.app_context():
        user.save_db()

        for key, val in user_info.items():
            res = getattr(user, key)
            assert res == val

        user_info = {
            "first_name": "NewName",
            "last_name": "NewLastname",
            "email": "test@mail.ru",
            "password": "newPass12345",
        }

        # test if required field is null
        assert Users(**user_info).save_db() is False

        # test dublicate emails
        user_info["user_name"] = "test_t"
        assert Users(**user_info).save_db() is False


def test_hash_func():
    strongpass = ""
    with pytest.raises(PasswordLength):
        get_secret_hash(strongpass)

    strongpass = "test12"
    with pytest.raises(PasswordLength):
        get_secret_hash(strongpass)

    strongpass = "test1234566"
    hashed_pass = get_secret_hash(strongpass)
    assert verify_secret(strongpass, hashed_pass)


def test_verify_pass_func():
    strongpass = "mystronpass"
    hashed_pass = get_secret_hash(strongpass)
    assert verify_secret(strongpass, hashed_pass)
    assert verify_secret("notoriginalPassword", hashed_pass) is False

    new_stronpas = "newpas"
    with pytest.raises(PasswordLength):
        verify_secret(new_stronpas, "dsfsadfaswerwr")

    with pytest.raises(ValueError):
        verify_secret("StrongPass", "eower23423424sdfsdf")


def test_user_pass_hash(new_user):
    _, user_info = new_user

    user = UserSchema().load(user_info)

    assert user.password != user_info["password"]
    for key, val in user_info.items():
        res = getattr(user, key)
        if key == "password":
            assert verify_secret(val, user.password)
            continue
        assert res == val


def test_user_from_db(init_db_users, app):
    with app.app_context():
        user = init_db_users.session.query(Users).get(1)
        user1 = init_db_users.session.query(Users).get(2)

        assert user.user_name == "shako"
        assert user.email == "test1@mail.ru"
        assert user.first_name == "Shehriyar"
        assert user.last_name == "Rzayev"
        assert verify_secret("Test12345", user.password)
        assert verify_secret("WrongPassword", user.password) is False

        assert user1.user_name == "sebuhi_sh"
        assert user1.email == "test2@mail.ru"
        assert user1.first_name == "Sebuhi"
        assert user1.last_name == "Shukurov"
        assert verify_secret("Test12345", user1.password)
        assert verify_secret("WrongPassword", user1.password) is False


def test_update_user_db(init_db_users, app):

    with app.app_context():
        user = init_db_users.session.query(Users).get(1)
        user.update(email="updated@mail.ru")

        assert user.email == "updated@mail.ru"

        user = init_db_users.session.query(Users).get(1)
        assert user.email == "updated@mail.ru"

        user.update(first_name="UpdatedName")
        assert user.first_name == "UpdatedName"

        user = init_db_users.session.query(Users).get(1)
        assert user.first_name == "UpdatedName"

        user.update(password="NewStrongPass12")
        assert "NewStrongPass12" == user.password

        user = init_db_users.session.query(Users).get(1)
        assert "NewStrongPass12" == user.password

        user_info = {
            "first_name": "NewName",
            "last_name": "NewLastname",
            "email": "newmail@mail.ru",
            "password": "newPass12345",
        }

        user.update(**user_info)

        for key, val in user_info.items():
            res = getattr(user, key)
            assert res == val

        user = init_db_users.session.query(Users).get(1)

        for key, val in user_info.items():
            res = getattr(user, key)
            assert res == val
