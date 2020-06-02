from api.views import  CreateUser,UserList,UserDetail, Todos,TodoOperations,Login,RefreshToken
from django.contrib.auth import get_user_model
from api.serializer import  UserSerializer
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from api.models import  Todo
from rest_framework.test import APITestCase
from django.urls import  reverse
import  pytest
User = get_user_model()



            
@pytest.mark.django_db
def create_user_test(client,setup):

    path = reverse("user_create")
        
    response = client.post(path,setup.get("user"),format='json')

    assert response.status_code == 201

    response_2 = client.post(path, setup.get("user"), format='json')
    
    assert response_2.status_code == 400 

    user = User.objects.filter(id=1).first()
    
    assert user.first_name == "test_user"
    assert user.username == "testname"
    assert user.email == "test@gmail.com"

@pytest.mark.django_db
def user_list_test(client):

    path = reverse("user_list")

    response = client.get(path)
    
    assert response.status_code == 200



def user_detail_test(client):
    user = User.objects.create(
        first_name="test_user",
        username="testname",
        password="test12345",
        email="test@gmail.com",
        last_name="testlastname"
    )

    path = reverse("user_detail",args="1")
    
    
    response = client.get(path,format='json')

    assert response.status_code == 200

    assert user.first_name == response.json().get("first_name") 
    assert user.username == response.json().get("username")
    assert user.email == response.json().get("email")
    assert user.last_name == response.json().get("last_name") 

                                                

def user_detail_test(client):
    path = reverse("user_detail",args="1")

    new_user = User.objects.create(
        first_name="test_user",
        username="testname",
        password="test12345",
        email="test@gmail.com",
        last_name="testlastname"
    )
    data = {"first_name": "TuralYek"}


    response = client.put(path,data,format='json')


    edited_user = User.objects.filter(id=1).first()

    assert response.status_code == 200

    assert edited_user.first_name == response.json().get("first_name")


@pytest.mark.django_db
def user_detail_test(client):

    new_user = User.objects.create(
        first_name="test_user",
        username="testname",
        password="test12345",
        email="test@gmail.com",
        last_name="testlastname"
    )

    path = reverse("user_detail",args="1")

    response = client.delete(path,format='json')
    assert response.status_code == 200 


    assert User.objects.filter(id=1).first() == None

 
@pytest.mark.django_db
def login_test(client):
    user = User.objects.create_user(
        username="test_user",
        password="test_password",
    )

    path = reverse("login")

    response = client.post(path,{"username":"test_user","password":"test_password"},format='json')
    

    assert response.status_code == 200
    
    assert ['access'] ==  [k for k,v in response.data.items() if k =="access" ]
    

    assert ['refresh'] == [k for k,v in response.data.items() if k =="refresh" ]

@pytest.mark.django_db
def missingfields_test(client):

    path = reverse("login")

    response = client.post(path,format='json')
    
    assert response.status_code == 400

@pytest.mark.django_db
def token_refresh_test(client):
    user = User.objects.create_user(
            username="test_user",
            password="test_password")

    path_login = reverse("login")
    path_token_refresh = reverse("token_refresh")

    response = client.post(path_login,{"username":"test_user","password":"test_password"},format='json')
    
    response_login = response.json()

    response_refresh = client.post(path_token_refresh,{"refresh":response_login.get("refresh")},format='json')
    

    assert response.status_code == 200

    assert response_refresh.status_code == 200




@pytest.mark.django_db
def post_todo_test(user_setUp):
    
    client = APIClient()

    path = reverse("user_todo")

    data = {
        "title": "Test Title",
        "description": "Test description"
    }

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.post(path,data,format='json')


    assert res.status_code == 201

    assert res.json().get("title") ==  data["title"]
    assert res.json().get("description") == data["description"]



@pytest.mark.django_db
def get_all_todos_test(user_setUp):
    client = APIClient()

    path = reverse("user_todo")

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.get(path,format='json')
    
    assert res.status_code == 200


@pytest.mark.django_db
def  todo_operation_test(user_setUp):
    client = APIClient()

    path = reverse("user_todo_operation",args="1")
    
    user_todo = reverse("user_todo")

    data = {
        "title": "Test Title",
        "description": "Test description"
    }

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.post(user_todo,data,format='json')


    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.get(path,format='json')
    
    assert res.status_code == 200
    assert res.json().get("id") == 1


@pytest.mark.django_db
def test_todo_operation_test(user_setUp):
    client = APIClient()

    path = reverse("user_todo_operation",args="1")
    
    user_todo = reverse("user_todo")

    data_1 = {
        "title": "Test Title",
        "description": "Test description"
    }

    data_2 = {
        "title": "Test Title2",
        "description": "Test description2"
    }

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.post(user_todo,data_1,format='json')


    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.get(path,format='json')
    assert res.json().get("title") == data_1["title"]

    res_2 =  client.put(path,data_2,format='json')


    assert res_2.json().get("title") == data_2["title"]

    assert res.status_code == 200

@pytest.mark.django_db
def todo_operation_test(user_setUp):
    client = APIClient()

    path = reverse("user_todo_operation",args="1")

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_setUp.get('access')}")

    res =  client.delete(path,format='json')
    
    assert res.status_code == 404
 
















