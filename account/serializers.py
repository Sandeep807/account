from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from django.utils.translation import activate
from .mail import *
from .models import *
import random

class UserSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','password','first_name','last_name','email']

    def create(self, validated_data):
        username=validated_data['username']
        password=validated_data['password']
        first_name=validated_data['first_name']
        last_name=validated_data['last_name']
        email=validated_data['email']

        obj=User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
        obj.set_password(password)
        obj.save()
        token=random.randint(10000,99999)
        activate_url=f'{token}'
        Profile.objects.create(user=obj,token=token)
        send_activate_email(obj.email,obj.first_name,activate_url)
        return obj

class ProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'