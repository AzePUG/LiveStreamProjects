from django.urls import  path
from .views import  UserDetail,UserList,CreateUser, Todos, TodoOperations,Login,RefreshToken
from rest_framework_simplejwt.views import token_refresh


urlpatterns = [

    path('users/<int:pk>/',UserDetail.as_view(),name="user_detail"),
    path('users/',UserList.as_view(),name="user_list"),
    path('user/',CreateUser.as_view(),name="user_create"),
    

    path("user/todos/",Todos.as_view(),name="user_todo"),#POST ,#GET all todos
    path("user/todos/<int:pk>/",TodoOperations.as_view(),name="user_todo_operation"), #PUT,GET,DELETE specifc

    path("login/", Login.as_view(),name="login"),
    path("token-refresh/", RefreshToken.as_view(),name="token_refresh")

]