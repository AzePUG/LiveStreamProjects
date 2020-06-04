from app.models import Todo, Users
from datetime import datetime
from app.app import app


def test_todo_class():
    todo_info = {"title": "testtitle", "description": "testdescription"}
    todo = Todo(**todo_info)
    for key, val in todo_info.items():
        res = getattr(todo, key)
        assert res == val


def test_todo_create(app, init_db_todos):
    with app.app_context():
        db = init_db_todos
        todo_info = {"title": "testtitle", "description": "testdescription"}
        new_todo = Todo(**todo_info)
        new_todo.save_db()

        todo = db.session.query(Todo).get(new_todo.id)
        assert todo.user_id is None

        for key, val in todo_info.items():
            res = getattr(todo, key)

            assert res == val

        todo_info = {
            "title": "testtitle",
            "description": "testdescription",
            "user_id": 1,
        }
        new_todo = Todo(**todo_info)
        new_todo.save_db()
        for key, val in todo_info.items():
            res = getattr(new_todo, key)
            assert res == val


def test_todo_update(app, init_db_todos):
    with app.app_context():
        db = init_db_todos

        todo = db.session.query(Todo).get(1)
        assert todo.description == "Learn Python with TechAcademy"
        assert todo.title == "Python"
        assert todo.user_id == 1

        todo.update(user_id=None)

        todo = db.session.query(Todo).get(1)
        assert todo.user_id is None
        assert todo.updated is not None

        todo.update(title="updatedtitle")

        todo = db.session.query(Todo).get(1)
        assert todo.title == "updatedtitle"

        todo.update(description="updateddescription")

        todo = db.session.query(Todo).get(1)
        assert todo.description == "updateddescription"
