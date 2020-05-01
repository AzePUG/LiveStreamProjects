from django.shortcuts import render
from django.http import  HttpResponse
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
# from .models import  User
from django.shortcuts import get_object_or_404
import  logging
from .utils import  LOGGING
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .serializer import  UserSerializer,UserSerializerDetails
from django.shortcuts import get_object_or_404

logging.config.dictConfig(LOGGING)

from django.contrib.auth import get_user_model


User = get_user_model()



#this endpoint will create user by using post method
class CreateUser(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            logging.info(f"New user Created")

            data = dict(serializer.data)
            data.pop("password")
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#this returns all users from the list
class UserList(APIView):
    permission_classes = [AllowAny] #allowing anyone to make request

    def get(self, request):
        
        user_list =   User.objects.all()[:20]
        
        data = UserSerializerDetails(user_list, many=True).data
                
        return Response(data)


#this enpoint has 3 methods either you can get user, delete, and update the user information
class UserDetail(APIView):
    permission_classes = [AllowAny]


    def get(self, request, pk):
        

        user_data = get_object_or_404(User, pk=pk)
        print(user_data)
        data = UserSerializerDetails(user_data).data
        return Response(data)

    def put(self, request, pk):

        # existing_user = get_object_or_404(User, pk=pk)
        existing_user = User.objects.filter(id=pk).first()

        if not existing_user:
            return Response({"result": False,"message": "No account found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(instance=existing_user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):

            serializer.save()
            data = dict(serializer.data)
            data.pop("password")
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        
        user.delete()
        
        logging.info(f"User deleted")

        return Response({"message": f"User with username {user.username} has been deleted"},status=status.HTTP_200_OK)

       