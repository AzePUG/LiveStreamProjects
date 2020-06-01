from api.views import  CreateUser,UserList,UserDetail, Todos,TodoOperations,Login,RefreshToken
from django.contrib.auth import get_user_model
from api.serializer import  UserSerializer
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from api.models import  Todo
from rest_framework.test import APITestCase
from django.urls import  reverse
User = get_user_model()




class TestUserViews(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = {
            "first_name": "test_user",
            "username":"testname",
            "password":"test12345",
            "email":"test@gmail.com",
            "last_name":"testlastname"
            }
        self.user_2 = {
            "first": "test_user",
            "username":"testname",
            "password":"test12345",
            "email":"test@gmailcom",
            "last_name":"testlastname"
            }

            

    def test_create_user(self):
        path = reverse("user_create")
        
        response = self.client.post(path,self.user,format='json')

        self.assertEqual(response.status_code, 201) 

        response_2 = self.client.post(path,self.user,format='json')
        
        self.assertEqual(response_2.status_code, 400) 

        user = User.objects.filter(id=1).first()
        
        self.assertEqual(user.first_name, "test_user") 
        self.assertEqual(user.username, "testname") 
        self.assertEqual(user.email, "test@gmail.com") 


        # print(response_2.json())
    
    def test_user_list(self):

        path = reverse("user_list")

        response = self.client.get(path)
        
        self.assertEqual(response.status_code, 200) 
    


    def test_user_detail_get(self):
        user = User.objects.create(
            first_name="test_user",
            username="testname",
            password="test12345",
            email="test@gmail.com",
            last_name="testlastname"
        )

        path = reverse("user_detail",args="1")
        
        
        response = self.client.get(path,format='json')

        self.assertEqual(response.status_code, 200) 

        self.assertEqual(user.first_name, response.json().get("first_name")) 
        self.assertEqual(user.username, response.json().get("username")) 
        self.assertEqual(user.email, response.json().get("email")) 
        self.assertEqual(user.last_name, response.json().get("last_name")) 

                                                

    def test_user_detail_put(self):
        path = reverse("user_detail",args="1")

        new_user = User.objects.create(
            first_name="test_user",
            username="testname",
            password="test12345",
            email="test@gmail.com",
            last_name="testlastname"
        )
        data = {"first_name": "TuralYek"}


        response = self.client.put(path,data,format='json')


        edited_user = User.objects.filter(id=1).first()

        self.assertEqual(response.status_code, 200) 

        self.assertEqual(edited_user.first_name, response.json().get("first_name")) 


    def test_user_detail_delete(self):

        new_user = User.objects.create(
            first_name="test_user",
            username="testname",
            password="test12345",
            email="test@gmail.com",
            last_name="testlastname"
        )

        path = reverse("user_detail",args="1")

        response = self.client.delete(path,format='json')
        self.assertEqual(response.status_code, 200) 


        self.assertIsNone(User.objects.filter(id=1).first())

 

    def test_login(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
        )

        path = reverse("login")

        response = self.client.post(path,{"username":"test_user","password":"test_password"},format='json')
        
   
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_missingfields(self):

        path = reverse("login")

        response = self.client.post(path,format='json')
        
        self.assertEqual(response.status_code, 400)



    def test_token_refresh(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password")

        path_login = reverse("login")
        path_token_refresh = reverse("token_refresh")

        response = self.client.post(path_login,{"username":"test_user","password":"test_password"},format='json')
        
        response_login =response.json()

        response_refresh = self.client.post(path_token_refresh,{"refresh":response_login.get("refresh")},format='json')
        

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response_refresh.status_code, 200)



class TestTodoViews(APITestCase):



    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
        )
        path_login = reverse("login")

        self.response = self.client.post(path_login,{"username":"test_user","password":"test_password"},format='json')
        
        self.response_login =self.response.json()

    def test_post_todo(self):
        path = reverse("user_todo")

        data = {
            "title": "Test Title",
            "description": "Test description"
        }
 
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.post(path,data,format='json')

   
        self.assertEqual(res.status_code, 201)

        self.assertEqual(res.json().get("title"), data["title"])
        self.assertEqual(res.json().get("description"), data["description"])




    def test_get_all_todos(self):
        path = reverse("user_todo")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.get(path,format='json')
        self.assertEqual(res.status_code, 200)



    def  test_todo_operation_get(self):
        
        path = reverse("user_todo_operation",args="1")
        
        user_todo = reverse("user_todo")

        data = {
            "title": "Test Title",
            "description": "Test description"
        }
 
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.post(user_todo,data,format='json')


        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.get(path,format='json')
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get("id"), 1)



    def  test_todo_operation_put(self):
        
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

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.post(user_todo,data_1,format='json')


        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.get(path,format='json')
        self.assertEqual(res.json().get("title"), data_1["title"])

        res_2 =  self.client.put(path,data_2,format='json')


        self.assertEqual(res_2.json().get("title"), data_2["title"])

        self.assertEqual(res.status_code, 200)

  
    def  test_todo_operation_delete(self):

        path = reverse("user_todo_operation",args="1")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.response_login.get('access')}")

        res =  self.client.delete(path,format='json')
        
        self.assertEqual(res.status_code, 404)
 

