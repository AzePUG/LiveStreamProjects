from django.test import  SimpleTestCase,TestCase
from django.urls import  reverse, resolve,include,path
from api.views import UserDetail,UserList,CreateUser,Todos,TodoOperations,Login,RefreshToken
from rest_framework.test import APITestCase, URLPatternsTestCase,APIRequestFactory
from rest_framework import status




#SimpleTestCase is just basic testing class that in case if you dont need to interact with DB

# APITestCase, 
# URLPatternsTestCase
# TestCase

#NOTE: be carefull django testcase works it looks basily what folder and files start with test work then class and functions. So in every class or function we should begin with Test keyword.

#AssertionError: Database queries to 'default' are not allowed in SimpleTestCase subclasses. Either subclass TestCase or TransactionTestCase to ensure proper test isolation or add 'default' to api.tests.test_paths.TestApiEndPoints.databases to silence this failure.

class TestApiEndPoints(TestCase):
 

    def test_api_users_path(self):
    
        path = reverse("user_detail",args="1")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, UserDetail)
        response = self.client.get(reverse("user_detail",args="1"),format='json')

        # print(response.data)
        # print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) #checking if it is 404

    
    def test_api_user_list_path(self):
        path = reverse("user_list")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, UserList)

        response = self.client.get(reverse("user_detail",args="1"),format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def test_api_user_create_path(self):
        path = reverse("user_create")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, CreateUser)

        response = self.client.post(reverse("user_create"),format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
    
    def test_api_user_todo_path(self):
        path = reverse("user_todo")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, Todos)

        response = self.client.post(reverse("user_todo"),format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
    
    def test_api_user_todo_operation_path(self):
        path = reverse("user_todo_operation",args="1")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, TodoOperations)

        response = self.client.post(path,format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_api_login_path(self):
        path = reverse("login")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, Login)

        response = self.client.post(reverse("login"),format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_api_toke_refresh_path(self):
        path = reverse("token_refresh")
        
        # print("the acutal path =>", path)

        self.assertEquals(resolve(path).func.view_class, RefreshToken)

        response = self.client.post(path,format='json')
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

