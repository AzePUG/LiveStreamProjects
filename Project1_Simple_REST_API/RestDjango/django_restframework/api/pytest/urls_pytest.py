
import pytest
from django.urls import  reverse, resolve

from django.contrib.auth import get_user_model
from api.models import Todo

User = get_user_model()

'''
client fixture is included with django, client  instance passed in whenever you add this as argument to your test funtions. BTW you can create your own fixture as well below an example:

@pytest.fixture
def fixture_test():
    return "Hello World!"

So the fucntion above, will allow us fixture_test add as an argument to any test function in our testsute So you can put that globally to acces accros project.

fixetures are powerfull
'''


@pytest.mark.django_db
def api_users_test(client):

    path = reverse("user_detail",args="1")
    response = client.get(path)
    assert response.status_code == 404

    assert resolve(path).func.view_class, UserDetail

 

@pytest.mark.django_db
def test_api_user_list_test(client):
    path = reverse("user_create")

    response = client.post(path)

    assert resolve(path).func.view_class, CreateUser

    assert response.status_code == 400

# @pytest.mark.django_db    
def api_user_todo_operation_test(client):
    path = reverse("user_todo_operation",args="1")

    response = client.post(path)

    assert response.status_code == 401
    assert resolve(path).func.view_class, TodoOperations


# @pytest.mark.django_db  
def api_login_path_test(client):
    path = reverse("login")
    
    response = client.post(path)

    assert response.status_code == 400
    assert resolve(path).func.view_class, Login

    print("the acutal path =>", path)


# @pytest.mark.django_db
def api_toke_refresh_path_test(client):
    path = reverse("token_refresh")
    
    response = client.post(path)

    assert resolve(path).func.view_class, RefreshToken

    assert response.status_code == 400 