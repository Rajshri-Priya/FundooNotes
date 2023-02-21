from django.contrib.auth import login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from logging_confiq.logger import get_logger
from user_auth.models import CustomUser
from user_auth.serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
# logging config
logger = get_logger()


# Create your views here.

class CustomUserRegistrationAPIView(APIView):
    serializer_class = CustomUserRegistrationSerializer

    @swagger_auto_schema(request_body=CustomUserRegistrationSerializer, operation_summary='POST User Registeration')
    def post(self, request):
        try:
            serializer = CustomUserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, "message": "user Registered Successfully", "data": serializer.data,
                             "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            user = CustomUser.objects.all()
            serializer = CustomUserRegistrationSerializer(user, many=True)
            return Response({"success": True, 'message': 'user Retrieve successfully!', 'Data': serializer.data,
                             "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    @swagger_auto_schema(request_body=CustomUserRegistrationSerializer, operation_summary='PUT User Registeration')
    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response({"success": True, 'message': 'user updated successfully!', 'Data': serializer.data,
                             "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    @swagger_auto_schema(request_body=CustomUserRegistrationSerializer, operation_summary='DELETE User Registeration')

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.delete()
            return Response({"success": True, "Message": "User Deleted Successfully"}, status=204)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


# *********************************user-login Apiview*****************

class CustomUserLoginAPIView(APIView):
    serializer_class = CustomUserLoginSerializer

    @swagger_auto_schema(request_body=CustomUserLoginSerializer, operation_summary='POST User Login')

    def post(self, request):
        try:
            serializer = CustomUserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            login(request, serializer.context.get('user'))
            return Response({"success": True, "message": "Login Successfully", "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


