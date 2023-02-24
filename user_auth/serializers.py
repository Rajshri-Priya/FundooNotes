import logging

from django.contrib.auth import authenticate, login
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
    """validation by manually"""

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        print(validated_data)
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        # is_active is property
        if not user:
            raise serializers.ValidationError("Incorrect Credentials")
        validated_data.update({'user': user})
        print(validated_data)
        self.context.update({'user': user})
        return user
