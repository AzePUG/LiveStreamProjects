from app.serializer import UserSchema, UpdateSchema
from app.utils import verify_secret, get_secret_hash
from app.models import Users
from marshmallow.exceptions import ValidationError
import pytest


def test_user_schema():
    mydata = {
        "first_name": "Shehriyar",
        "last_name": "Rzayev",
        "user_name": "shako",
        "email": "test1@mail.ru",
        "password": "Test12345",
    }

    verifed_data = UserSchema().load(mydata)

    for key, value in mydata.items():
        res = getattr(verifed_data, key)
        if key == "password":
            assert verify_secret(value, res)
            continue
        assert res == value


def test_schema_update(init_db_users, app):

    with app.app_context():
        user = init_db_users.session.query(Users).get(1)
        schema = UpdateSchema()
        user_info = schema.load(dict(email="updated@mail.ru"))
        user.update(**user_info)
        assert user.email == "updated@mail.ru"

        user = init_db_users.session.query(Users).get(1)
        assert user.email == "updated@mail.ru"

        user_info = schema.load(dict(first_name="UpdatedName"))

        user.update(**user_info)
        assert user.first_name == "UpdatedName"

        user = init_db_users.session.query(Users).get(1)
        assert user.first_name == "UpdatedName"

        user_info = schema.load(dict(password="NewStrongPass12"))
        user.update(**user_info)
        assert verify_secret("NewStrongPass12", user.password)

        user = init_db_users.session.query(Users).get(1)
        assert verify_secret("NewStrongPass12", user.password)

        user_info = {
            "first_name": "NewName",
            "last_name": "NewLastname",
            "email": "newmail2@mail.ru",
            "password": "newPass12345",
        }

        loaded_data = schema.load(user_info)
        user.update(**loaded_data)

        for key, val in user_info.items():
            res = getattr(user, key)
            if key == "password":
                assert verify_secret(val, user.password)
                continue
            assert res == val

        user = init_db_users.session.query(Users).get(1)

        for key, val in user_info.items():
            res = getattr(user, key)
            if key == "password":
                assert verify_secret(val, user.password)
                continue
            assert res == val

        # data = {
        #     "first_name": "testname",
        #     "last_name": "testsurname",
        # }

        # loaded_data = schema.load(data)
        # user.update(**loaded_data)

        # user_info.update(data)

        # for key, val in user_info.items():
        #     res = getattr(user, key)
        #     if key == "password":
        #         assert verify_secret(val, user.password)
        #         continue
        #     assert res == val

        # user = init_db_users.session.query(Users).get(1)

        # for key, val in user_info.items():
        #     res = getattr(user, key)
        #     if key == "password":
        #         assert verify_secret(val, user.password)
        #         continue
        #     assert res == val


def test_user_schema_valid(invalid_data):
    schema = UserSchema()

    with pytest.raises(ValidationError):
        for data in invalid_data:
            schema.load(data)
