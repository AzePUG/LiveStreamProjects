from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.contrib.auth import password_validation
from .models import  Todo

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields =("first_name", "last_name", "email","username","password")

        #making this fields to be reuired
        extra_kwargs = {
            'first_name': {'required': True},
            "last_name":{'required': True},
            "email":{'required': True},
            "username":{'required': True},
            "password": {'required': True}} 

    #validate user password with deault django password validator
    #You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer subclass. These are similar to the .clean_<field_name> methods on Django forms.These are similar to the .clean_<field_name> methods on Django forms.
    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value
    
    #overwriting create method
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    #overwriting update method
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        user = super(UserSerializer, self).update(instance, validated_data)
        if password: 
            user.set_password(validated_data.get('password'))
        user.save()
        return user

#for user details
class UserSerializerDetails(serializers.ModelSerializer):
    class Meta:
        model = User

        fields =("first_name", "last_name", "email","username","id")
    

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo

        fields = ("id","user","title","description",)

    