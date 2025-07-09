from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model= User
        fields = ['id','email', 'username', 'password', 'name', 'phone', 'location']

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= ['id', 'email', 'username', 'name', 'phone', 'location']