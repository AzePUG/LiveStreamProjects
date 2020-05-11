from django.urls import  path
from .views import  UserDetail,UserList,CreateUser, Todos, TodoOperations,Login
from rest_framework_simplejwt.views import token_refresh


urlpatterns = [

    path('users/<int:pk>/',UserDetail.as_view()),
    path('users/',UserList.as_view()),
    path('user/',CreateUser.as_view()),

    path("user/todo/",Todos.as_view()),#POST ,#GET all todos
    path("user/todo/<int:pk>/",TodoOperations.as_view()), #PUT,GET,DELETE specifc

    path("login/", Login.as_view()),
    path("token-refresh/", token_refresh)

]
