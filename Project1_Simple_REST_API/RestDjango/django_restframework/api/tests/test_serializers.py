from django.test import TestCase
from api.serializer import UserSerializer,UserSerializerDetails,TodoSerializer
from api.models import  Todo
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserSerializers(TestCase):
    

    def setUp(self):

        self.user_data = {
            "first_name":"TestName",
            "last_name":"TestSurname",
            "username":"testuser", 
            "email":"test@gmail.com",
            "password":"test12345"
        }
        
     
        self.user_serializer = UserSerializer(instance=self.user_data)

    def test_user_serializer_fields(self):
        data = self.user_serializer.data


        self.assertEqual(data['first_name'], self.user_data["first_name"])
        self.assertEqual(data['last_name'], self.user_data["last_name"])
        self.assertEqual(data['username'], self.user_data["username"])
        self.assertEqual(data['password'], self.user_data["password"])
        self.assertEqual(data['first_name'], self.user_data["first_name"])



    def test_validate_password(self):
        

        data = self.user_serializer.data

        self.assertTrue(self.user_serializer.validate_password(data["password"]),self.user_data["password"])
        
    def test_is_valid(self):
  
        user_serializer = UserSerializer(data=self.user_data)

        self.assertTrue(user_serializer.is_valid())
        
        self.assertTrue(self.user_serializer.create(user_serializer.validated_data))


        with self.assertRaises(Exception):
            self.assertTrue(user_serializer.save())



    def test_update(self):
        initial_data = {
            'first_name': "initial_test",
            "last_name": "intial_surname",
            "email": "intialtest@gmail.com",
            "username": "intialtestuser",
            "password": "intial12345"
            } 

        new_data = {
            'first_name': "new_test",
            "last_name": "test_surname",
            "email": "test@gmail.com",
            "username": "newtestuser",
            } 
        user_ = User.objects.create(**initial_data)

        update_serializer = UserSerializer(instance=user_, data=new_data, partial=True)

        self.assertTrue(update_serializer.is_valid())
        
        self.assertTrue(update_serializer.save())
        new_user_db = User.objects.filter(id=1).first()

        
        self.assertEqual(new_user_db.username, "newtestuser")
        self.assertEqual(new_user_db.last_name,"test_surname")
        self.assertEqual(new_user_db.first_name,"new_test")
        self.assertEqual(new_user_db.email,"test@gmail.com")




class TestTodoSerializers(TestCase):

    
    def setUp(self):

        self.user_data = {
            "first_name":"TestName",
            "last_name":"TestSurname",
            "username":"testuser", 
            "email":"test@gmail.com",
            "password":"test12345"
        }

        self.todo_data = {
            "title": "Test Title",
            "description": "Test description"
        }
        
        self.user = User.objects.create(**self.user_data)

        
        self.todo_data["user"] = self.user

        self.todo_seriralizer = TodoSerializer(instance=self.todo_data)

    def test_todo_serializer_fields(self):

        data = self.todo_seriralizer.data

        self.assertEqual(data['title'],self.todo_data["title"])

        self.assertEqual(data['description'],self.todo_data["description"])

        self.assertEqual(data['user'], self.user.id)


    def test_is_valid(self):


        self.todo_data["user"]  = self.user.id

        todo_serializer = TodoSerializer(data=self.todo_data)

        self.assertTrue(todo_serializer.is_valid())
        
        self.assertTrue(todo_serializer.save())



     

  
        

 