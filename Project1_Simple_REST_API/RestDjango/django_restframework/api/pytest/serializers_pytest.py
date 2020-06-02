import pytest
from api.serializer import  UserSerializer,UserSerializerDetails,TodoSerializer
from api.models import Todo
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()








def check_test(user_serlize):


    assert user_serlize.data['first_name'] == "TestName"
    assert user_serlize.data['last_name'] == "TestSurname"
    assert user_serlize.data['username'] == "testuser"
    assert user_serlize.data['email'] == "test@gmail.com"
    assert user_serlize.data['password'] == "test12345"



def validate_password_test(user_serlize):
    
    
    assert user_serlize.validate_password(user_serlize.data['password']) == user_serlize.data['password']

@pytest.mark.django_db
def is_valid_test(data):

  
    user_serializer = UserSerializer(data=data)

    assert user_serializer.is_valid() == True
    
    assert user_serializer.create(user_serializer.validated_data)  ==User.objects.filter(id=1).first()

    with pytest.raises(Exception) as error:

        user_serializer.save()

        assert user.username == "testuser"
            
    assert error.type == IntegrityError


@pytest.fixture
def update_func():
    temp = [{
        'first_name': "initial_test",
        "last_name": "intial_surname",
        "email": "intialtest@gmail.com",
        "username": "intialtestuser",
        "password": "intial12345"
    },
    {
    'first_name': "new_test",
    "last_name": "test_surname",
    "email": "test@gmail.com",
    "username": "newtestuser",
    }]


    return temp


@pytest.mark.django_db
def update_test(update_func):

        user_ = User.objects.create(**update_func[0])

        update_serializer = UserSerializer(instance=user_, data=update_func[1], partial=True)

        assert  update_serializer.is_valid()  == True
        
        assert  update_serializer.save() == User.objects.filter(id=1).first()
        new_user_db = User.objects.filter(id=1).first()

        
        assert new_user_db.username == "newtestuser"
        assert new_user_db.last_name == "test_surname"
        assert new_user_db.first_name =="new_test"
        assert new_user_db.email  == "test@gmail.com"






@pytest.fixture
def saved_user():
    user_data = {
            "first_name":"TestName",
            "last_name":"TestSurname",
            "username":"testuser", 
            "email":"test@gmail.com",
            "password":"test12345"
        }
        

   
    user = User.objects.create(**user_data)

    return user
       


@pytest.fixture
@pytest.mark.django_db
def todo_fucntion(saved_user):
    todo_data = {
            "title": "Test Title",
            "description": "Test description"
        } 
 
    todo_data["user"] = saved_user

    todo = todo_seriralizer = TodoSerializer(instance=todo_data)

    return todo


@pytest.mark.django_db
def todo_serializer_fields_test(todo_fucntion):


    assert todo_fucntion.data['title'] == "Test Title"

    assert todo_fucntion.data['description'] == "Test description"

    assert todo_fucntion.data['user'] ==  User.objects.get(id=1).id


@pytest.mark.django_db
def is_valid_test(todo_fucntion):
 
    todo_serializer = TodoSerializer(data={"title":"Test Title", "description": "Test description" })

    assert todo_serializer.is_valid() == True
    
    assert todo_serializer.save()  == Todo.objects.get(id=1)



     

