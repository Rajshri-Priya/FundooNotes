import logging

from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.models import CustomUser
from user_auth.serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer


# Create your views here.


class CustomUserRegistrationAPIView(APIView):

    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registered Successfully", "data": serializer.data, "status": 201}, status=201)

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = CustomUserRegistrationSerializer(user, many=True)
        return Response(serializer.data)
    #
    # def put(self, request):
    #     pk = request.data.get('id')
    #     user = CustomUser.objects.get(id=pk)
    #     serializer = self.serializer_class(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'user updated successfully!', 'Data': serializer.data})
    #     return Response(serializer.errors, status=400)
    #
    # def delete(self, request):
    #     pk = request.data.get('id')
    #     user = CustomUser.objects.get(id=pk)
    #     user.delete()
    #     return Response({"Message": "User Deleted Successfully"}, status=204)


# *********************************user-login Apiview*****************

class CustomUserLoginAPIView(APIView):
    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({"message": "Login Successfully",
                             "username": user.username,
                             "email": user.email
                             }, status=201 )
        return Response({"message": "Login failed", "status": 202})
