from app.serializer import TodoSchema, TodoUpdateSchema
from app.models import Users, Todo
from marshmallow.exceptions import ValidationError
from app.app import app
import pytest


def test_todo_schema():
    mydata = {"title": "Python", "description": "Learn Python with TechAcademy"}

    verifed_data = TodoSchema().load(mydata)

    for key, value in mydata.items():
        res = getattr(verifed_data, key)
        if key == "password":
            assert res == value


def test_schema_update(init_db_todos, app):

    with app.app_context():
        todo = init_db_todos.session.query(Todo).get(1)
        schema = TodoUpdateSchema()
        todo_info = schema.load(dict(title="updatedtitle"))
        todo.update(**todo_info)
        assert todo.title == todo_info.get("title")

        todo = init_db_todos.session.query(Todo).get(1)
        assert todo.title == "updatedtitle"

        todo_info = schema.load(dict(description="UpdatedDescription"))

        todo.update(**todo_info)
        assert todo.description == todo_info.get("description")

        todo = init_db_todos.session.query(Todo).get(1)
        assert todo.description == "UpdatedDescription"

        mydata = {"title": "Python", "description": "Learn Python with TechAcademy"}
        loaded_data = schema.load(mydata)
        todo = todo.update(**loaded_data)
        for key, val in mydata.items():
            res = getattr(todo, key)
            assert res == val

        todo = init_db_todos.session.query(Todo).get(1)

        for key, val in mydata.items():
            res = getattr(todo, key)
            assert res == val


def test_todo_schema_valid(invalid_data_todos):
    schema = TodoSchema()

    with pytest.raises(ValidationError):
        for data in invalid_data_todos:
            schema.load(data)
