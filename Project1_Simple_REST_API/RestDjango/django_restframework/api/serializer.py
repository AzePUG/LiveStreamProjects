from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

from rest_framework.response import Response


#serilizing the user object
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


