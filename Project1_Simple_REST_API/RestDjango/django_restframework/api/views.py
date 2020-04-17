from django.shortcuts import render
from django.http import  HttpResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
# from .serializer import  UserSerializer
# from .models import  User
from django.shortcuts import get_object_or_404
import  logging
from .utils import  LOGGING
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

logging.config.dictConfig(LOGGING)




#massiv
users = []
id = 0 # id for each user

#using global key word to keep data not only inside func
def add_user(data):
    global id

    data["id"]=id
    users.append(data)
        
    id += 1
    print(id)

print(users)


def user_operations(pk, delete=False):
    if not delete:
        for user  in users:
            if user["id"] ==pk:
                return user
        return False
    else:

        for index, value  in enumerate(users):
            if value.get("id") == pk:
                del users[index]


            return True

        return False
#updateting user information
def update_user(data,pk):

   
    for index,value in enumerate(users):
        if value.get("id") == pk:
            value.update(data)
            users[index] = value     
            
            return True
    return False


#this endpoint will create user by using post method
class CreateUser(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        if not (request.data.get("first_name") and request.data.get("last_name") and request.data.get("user_name")):
            return Response({"result":False,"message":"User cannot be created"})

        add_user(request.data)   

        logging.info(f"New user Created")

        return Response({"user":f"user with username {request.data.get('user_name')} created"}, status=201)


#this returns all users from the list
class UserList(APIView):
    permission_classes = [AllowAny] #allowing anyone to make request

    def get(self, request):

        return Response(users)



#this enpoint has 3 methods either you can get user, delete, and update the user information
class UserDetail(APIView):
    permission_classes = [AllowAny]


    def get(self, request, pk):

        user = user_operations(pk)

        if user:
            return Response(user)

        return Response({"result":False, "message": "no user found"})

    def put(self, request, pk):

        if not (request.data.get("first_name") and request.data.get("last_name") and request.data.get("user_name")):
            return Response({"result":False,"message":"User cannot be created"})

        up = update_user(request.data,pk)
        if up:
            logging.info(f"User updated")

            return Response({"user":"updated"})

        return Response({"result":False, "message": "no user found"})
            

    def delete(self, request, pk):

        user = user_operations(pk,delete=True)

        if user:
            logging.info(f"User deleted")

            return Response({"result": "success"})
        
        return Response({"result": False, "message":"user not found"})


@api_view(['GET'])
def api(request):
    return Response({"result": True})
