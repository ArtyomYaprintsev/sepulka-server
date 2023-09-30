from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "is_staff", "role")
        read_only_fields = ("is_staff",)
