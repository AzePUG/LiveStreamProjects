from django.shortcuts import render
from django.http import  HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import  logging
from .utils import  LOGGING
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view
from .serializer import  UserSerializer,UserSerializerDetails, TodoSerializer
from django.shortcuts import get_object_or_404
from .models import Todo
from django.contrib.auth import get_user_model
from .utils import jwt_decode_handler
from rest_framework_simplejwt.views import  TokenObtainPairView,TokenRefreshView

logging.config.dictConfig(LOGGING)
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
        # print(user_data)
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
            
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        
        user.delete()
        
        logging.info(f"User deleted")

        return Response({"message": f"User with username {user.username} has been deleted"},status=status.HTTP_200_OK)

       

class Todos(APIView): 
    permission_classes = [IsAuthenticated]


    def post(self, request):
         
        token = request.headers.get("Authorization").split(" ")[1]

        details = jwt_decode_handler(token)
        user_id = details.get("user_id")

        if not User.objects.filter(id=user_id).last(): return Response({"message": "No such a user found"},status=status.HTTP_404_NOT_FOUND)

        request.data["user"] = user_id
        serializer = TodoSerializer(data=request.data)
    
      
        
        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request):
        token = request.headers.get("Authorization").split(" ")[1]

        details = jwt_decode_handler(token)
      

        user_id = details.get("user_id")
        
        if not User.objects.filter(id=user_id).last(): return Response({"error": True,"message": "No such a user found"},status=status.HTTP_404_NOT_FOUND)

    
        todos =  Todo.objects.filter(user=user_id).all()
        if not todos: return Response({"message":"No todos found for this user"})
        data = TodoSerializer(todos, many=True).data
                
        return Response(data)
    

class TodoOperations(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,pk):
        
        token = request.headers.get("Authorization").split(" ")[1]
        details = jwt_decode_handler(token)

        if not (User.objects.filter(id=details.get("user_id")).last() and Todo.objects.filter(id=pk).last()): return Response({"message": "No such a user or todo"},status=status.HTTP_404_NOT_FOUND)  

        todo = Todo.objects.filter(id=pk).first()

      

        serializer = TodoSerializer(instance=todo, data=request.data, partial=True)

        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data)
        
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request,pk):
        
        token = request.headers.get("Authorization").split(" ")[1]

        details = jwt_decode_handler(token)

        if not (User.objects.filter(id=details.get("user_id")).last() and Todo.objects.filter(id=pk).last()): return Response({"message": "No such a user or todo"},status=status.HTTP_404_NOT_FOUND)  

        todo = Todo.objects.filter(id=pk).last()
        
        todo.delete()
        

        return Response({"status": "OK", "message": "Todo has been deleted"})


    def get(self,request,pk):

        token = request.headers.get("Authorization").split(" ")[1]

        details = jwt_decode_handler(token)


        if not (User.objects.filter(id=details.get("user_id")).last() and Todo.objects.filter(id=pk).last()): return Response({"message": "No such a user or todo"},status=status.HTTP_404_NOT_FOUND)  
        
        todos =  Todo.objects.filter(id=pk,user=details.get("user_id")).last()
        
        if not todos:  return Response({"message":"no todos found"}, status=status.HTTP_404_NOT_FOUND) 

        data = TodoSerializer(todos).data
                
        return Response(data)




class Login(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        
>>>>>> master
        data = super().post(request, *args, **kwargs)

        data = data.data

        acces_token = jwt_decode_handler(data.get("access"))
        ref = jwt_decode_handler(data.get("refresh"))
        acces_token = jwt_decode_handler(data.get("access"))

        if not User.objects.filter(id=acces_token.get("user_id")).last(): return Response({"error": True,"message": "No such a user"},status=status.HTTP_404_NOT_FOUND)  
        
        todos =  Todo.objects.filter(user=acces_token.get("user_id")).all()
        
        todos = TodoSerializer(todos, many=True).data
        user =  User.objects.filter(id=acces_token.get("user_id")).last()
        
        user_details = UserSerializerDetails(user)


        data["todos"] = todos
        data["user_details"] = user_details.data

            
        return Response(data)

class RefreshToken(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)

        new_token = data.data
        # print(new_token)
        acces_token = jwt_decode_handler(new_token.get("access"))
        ref = jwt_decode_handler(new_token.get("refresh"))
        # print(ref)
        # print(acces_token)

        return Response(data)
