from app.serializer import UserSchema,UpdateSchema
from app.utils import verify_secret
from app.models import Users

def test_user_class(new_user):
    user,user_info = new_user

    for key,val in user_info.items():
        res = getattr(user,key)
        assert res == val


def test_create_user(flask_app,new_user,init_db):
    user,user_info = new_user
    with flask_app.app_context():
        user.save_db()
        print(user.id)
        
    for key,val in user_info.items():
        res = getattr(user,key)
        assert res == val
    


def test_pass_hash(new_user):
    _,user_info = new_user

    user = UserSchema().load(user_info)
    
    assert user.password != user_info["password"]
    for key,val in user_info.items():
        res = getattr(user,key)
        if key == "password":
            assert verify_secret(val,user.password)
            continue
        assert res == val


def test_user_from_db(init_db,flask_app):
    with flask_app.app_context():
        user = init_db.session.query(Users).get(1)
        user1 = init_db.session.query(Users).get(2)

        assert user.user_name == "shako"
        assert user.email == "test1@mail.ru"
        assert user.first_name == "Shehriyar"
        assert user.last_name == "Rzayev"
        
        assert user1.user_name == "sebuhi_sh"
        assert user1.email == "test2@mail.ru"
        assert user1.first_name == "Sebuhi"
        assert user1.last_name == "Shukurov"

def test_update_user_db(init_db,flask_app):
    
    with flask_app.app_context():
        user = init_db.session.query(Users).get(1)
        schema = UpdateSchema()
        user_info = schema.load(dict(email="updated@mail.ru"))
        user.update(**user_info)

        assert user.email == "updated@mail.ru"

        user = init_db.session.query(Users).get(1)
        assert user.email == "updated@mail.ru"

        user_info = schema.load(dict(first_name="UpdatedName"))

        user.update(**user_info)
        assert user.first_name == "UpdatedName"

        user = init_db.session.query(Users).get(1)
        assert user.first_name == "UpdatedName"

        user_info = schema.load(dict(password="NewStrongPass12"))
        user.update(**user_info)
        assert verify_secret("NewStrongPass12",user.password)
        
        user = init_db.session.query(Users).get(1)
        assert verify_secret("NewStrongPass12",user.password)

        user_info = {
            "first_name": "Bulk_name",
            "last_name" : "Bulk_lastname",
            "email": "bulkmail@mail.ru",
            "password": "bulkPass12345"
        }
        loaded_data = schema.load(user_info)
        user.update(**loaded_data)

        for key,val in user_info.items():
            res = getattr(user,key)
            if key == "password":
                assert verify_secret(val,user.password)
                continue
            assert res == val

        user = init_db.session.query(Users).get(1)

        for key,val in user_info.items():
            res = getattr(user,key)
            if key == "password":
                assert verify_secret(val,user.password)
                continue
            assert res == val

