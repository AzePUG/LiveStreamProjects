import pytest
from app.models import Users, Todo
from app.app import app as flask_app
from extensions.extension import db
from app.serializer import UserSchema, TodoSchema
from sqlalchemy.engine import reflection
from sqlalchemy import MetaData, Table, ForeignKeyConstraint
from sqlalchemy.schema import DropConstraint, DropTable


def db_DropEverything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    transactional = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    metadata = MetaData()

    tables = []
    all_foreign_keys = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk["name"]:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk["name"]))
        t = Table(table_name, metadata, *fks)
        tables.append(t)
        all_foreign_keys.extend(fks)

    for foreignkey in all_foreign_keys:
        conn.execute(DropConstraint(foreignkey))

    for table in tables:
        conn.execute(DropTable(table))

    transactional.commit()


@pytest.fixture()
def new_user():
    user_info = {
        "first_name": "Tural",
        "last_name": "Muradov",
        "user_name": "tural_m",
        "email": "test@mail.ru",
        "password": "Test12345",
    }
    user = Users(**user_info)
    return user, user_info


@pytest.fixture()
def client(app):

    test_client = app.test_client()
    yield test_client


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture()
def init_db_users(app):
    db.create_all()
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
    print(users)
    user = UserSchema().load(users[0])
    user1 = UserSchema().load(users[1])

    db.session.add(user)
    db.session.add(user1)
    db.session.commit()

    yield db
    db.close_all_sessions()
    db_DropEverything(db)


@pytest.fixture()
def invalid_data():
    invalid_data1 = {
        "testdata": "testvalue",
        "first_name": "NewName",
        "last_name": "NewLastname",
        "user_name": "Test_name",
        "email": "newmail2@mail.ru",
        "password": "newPass12345",
    }

    invalid_data2 = {
        "last_name": "NewLastname",
        "email": "newmail2@mail.ru",
        "password": "newPass12345",
    }

    invalid_data3 = {
        "first_name": "N",
        "user_name": "Test_name",
        "last_name": "New",
        "email": "newmail2@mail.ru",
        "password": "newPass12345",
    }

    yield [invalid_data1, invalid_data2, invalid_data3]


@pytest.fixture()
def init_db_todos(app):
    db.create_all()
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

    user = UserSchema().load(users[0])
    user1 = UserSchema().load(users[1])

    db.session.add(user)
    db.session.add(user1)
    db.session.commit()

    todos = [
        {
            "title": "Python",
            "description": "Learn Python with TechAcademy",
            "user_id": user.id,
        },
        {"title": "Python", "description": "Learn Python", "user_id": user1.id},
    ]

    todo = TodoSchema().load(todos[0])
    todo1 = TodoSchema().load(todos[1])

    db.session.add(todo)
    db.session.add(todo1)
    db.session.commit()

    yield db
    db.close_all_sessions()

    db_DropEverything(db)


@pytest.fixture()
def invalid_data_todos():

    invalid_data1 = {
        "title": "Python",
        "user_id": 1,
    }

    invalid_data2 = {"title": "Python"}

    invalid_data3 = {
        "title": "Python",
        "description": "Learn Python",
        "test": "testvalue",
    }

    yield [invalid_data1, invalid_data2, invalid_data3]
