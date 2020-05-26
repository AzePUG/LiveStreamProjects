import pytest
from app.models import Users
from app_init.app_factory import create_app
from extensions.extension import db
from app.serializer import UserSchema
from sqlalchemy.engine import reflection
from sqlalchemy import MetaData, Table, ForeignKeyConstraint
from sqlalchemy.schema import DropConstraint, DropTable


def remove_foreign_keys(db):

    inspector = reflection.Inspector.from_engine(db.engine)
    fake_metadata = MetaData()

    fake_tables = []
    all_fks = []

    for table_name in db.metadata.tables:
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if fk["name"]:
                fks.append(ForeignKeyConstraint((), (), name=fk["name"]))
        t = Table(table_name, fake_metadata, *fks)
        fake_tables.append(t)
        all_fks.extend(fks)

    connection = db.engine.connect()
    transaction = connection.begin()
    for fkc in all_fks:
        connection.execute(DropConstraint(fkc))
    transaction.commit()


def db_DropEverything(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk["name"]:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk["name"]))
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


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
def client():
    app = create_app("test")
    test_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield test_client

    ctx.pop()


@pytest.fixture()
def flask_app():
    app = create_app("test")
    ctx = app.app_context()
    ctx.push()
    yield app

    ctx.pop()


@pytest.fixture()
def init_db(flask_app):
    with flask_app.app_context():
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

        yield db
        db_DropEverything(db)
        # db.drop_all()
