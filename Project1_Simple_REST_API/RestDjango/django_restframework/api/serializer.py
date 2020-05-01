from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.contrib.auth import password_validation


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
    