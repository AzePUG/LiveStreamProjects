from django.urls import  path
from .views import  *


urlpatterns = [

    path('users/<int:pk>/',UserDetail.as_view()),
    path('users/',UserList.as_view()),
    path('user/',CreateUser.as_view()),

]
