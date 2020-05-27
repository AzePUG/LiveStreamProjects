
# What is test actually ? 
# Test is piece of code that makes sure that code you wrote works perfectly under speicif conditions

# main reason companies requires test: more quality meaning application without bugs, make sure peiace code working correctly


#There types of Tests exists:
 
# 1) Unit Test
# 2) Integration Test
# 3) Functional Test

# 1) Testing one piece independently of another code, we need to assert function reterun value

# 2) Tetsing multiple part of your code that integrated with each other

# 3) Functional test is actullay testing applications from end user point view, basicly it is done by selinum,what user will type or fill gthe form

from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import  Todo
from django.db.utils import IntegrityError

User = get_user_model()

class TestModels(TestCase):

    def setUp(self):

        self.user = User.objects.create(username="testuser", email="test@gmail.com")

    
    def test_user_model(self):
 
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email,"test@gmail.com")
    

    def test_todo_model(self):
        self.todo = Todo.objects.create(
           user=self.user,
           title="Test title",
           description="Test description" 
        )
        
       
        self.assertEqual(self.todo.user.username, "testuser")
        self.assertEqual(self.todo.title,"Test title")
        self.assertEqual(self.todo.description,"Test description")


    def test_new_insert(self):
        
        with self.assertRaises(Exception) as raised:  # top level exception as we want to figure out its exact type
            new_user = User.objects.create(username="testuser", email="test@gmail.com")
        self.assertEqual(IntegrityError, type(raised.exception))  


