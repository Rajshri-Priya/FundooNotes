import logging

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response

from .models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'phone', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        # is_active is property
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")
        return user
