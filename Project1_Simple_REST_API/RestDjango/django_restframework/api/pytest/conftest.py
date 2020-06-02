import pytest
from api.serializer import  UserSerializer
from django.contrib.auth import get_user_model
from api.models import Todo
from django.db.utils import IntegrityError
from django.urls import  reverse, resolve

User = get_user_model()
#wherner we need to run some code before test we use pytets fixture

# You can test your Django application without using a Library but pytest offers some features that are not present in Django’s standard test mechanism: :
# Detailed info on failing assert statements (no need to remember self.assert* names);
# Auto-discovery of test modules and functions;
# Modular fixtures for managing small or parametrized long-lived test resources;
# Can run unit test (including trial) and nose test suites out of the box;
#to run test with multiple markeers use dec  

#wherner we need to run some code before test we use pytets fixture

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



@pytest.fixture
def user_serlize():
    user_data = {
        "first_name":"TestName",
        "last_name":"TestSurname",
        "username":"testuser", 
        "email":"test@gmail.com",
        "password":"test12345"
    }
    
    
    user_serializer = UserSerializer(instance=user_data)
    return user_serializer

@pytest.fixture
def data():
    user_data = {
        "first_name":"TestName",
        "last_name":"TestSurname",
        "username":"testuser", 
        "email":"test@gmail.com",
        "password":"test12345"
    }
    return user_data


@pytest.fixture
def user_setUp(client):

    user = User.objects.create_user(
        username="test_user",
        password="test_password",
    )
    path_login = reverse("login")

    response = client.post(path_login,{"username":"test_user","password":"test_password"},format='json')
    
    return response.json()



@pytest.fixture
def setup():
    data = {
        "user":{
        "first_name": "test_user",
        "username":"testname",
        "password":"test12345",
        "email":"test@gmail.com",
        "last_name":"testlastname"
        },
        "user_2":{
        "first": "test_user",
        "username":"testname",
        "password":"test12345",
        "email":"test@gmailcom",
        "last_name":"testlastname"}
    }
    return data

