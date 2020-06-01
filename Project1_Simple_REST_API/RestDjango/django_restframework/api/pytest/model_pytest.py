import pytest
from django.db import models
from django.contrib.auth import get_user_model
from api.models import Todo
from django.db.utils import IntegrityError

User = get_user_model()

'''

You can use pytest marks to tell pytest-django your test needs database access:
import pytest

It is also possible to mark all tests in a class or module at once. This demonstrates all the ways of marking, even
though they overlap. Just one of these marks would have been sufficient. See t
'''

@pytest.fixture
def created_user():

    user = User.objects.create(username="testuser", email="test@gmail.com")
    return user


@pytest.fixture
@pytest.mark.django_db
def create_todo(created_user):
    todo = Todo.objects.create(
           user=created_user,
           title="Test title",
           description="Test description" 
        )
    return todo


@pytest.mark.django_db
def my_user_test(created_user):
    
    assert created_user.username == "testuser"

    assert created_user.email == "test@gmail.com"



@pytest.mark.django_db
def todo_model_test(create_todo):

    assert create_todo.user.username == "testuser"
    assert create_todo.title ==  "Test title"
    assert create_todo.description == "Test description"

    
        
       
       
@pytest.mark.django_db
def new_test(created_user):
    with pytest.raises(IntegrityError) as error:
        user = User.objects.create(username="testuser", email="test@gmail.com")

        assert user.username == "testuser"
        
    assert error.type == IntegrityError