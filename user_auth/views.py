from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from logging_confiq.logger import get_logger
from user_auth.models import CustomUser
from user_auth.serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer

# logging config
logger = get_logger()


# Create your views here.

class CustomUserRegistrationAPIView(APIView):
    serializer_class = CustomUserRegistrationSerializer

    def post(self, request):
        try:
            serializer = CustomUserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Registered Successfully", "data": serializer.data, "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)


    def get(self, request):
        try:
            user = CustomUser.objects.all()
            serializer = CustomUserRegistrationSerializer(user, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)

    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            serializer = self.serializer_class(user, data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response({'message': 'user updated successfully!', 'Data': serializer.data})
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.delete()
            return Response({"Message": "User Deleted Successfully"}, status=204)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)


# *********************************user-login Apiview*****************

class CustomUserLoginAPIView(APIView):
    serializer_class = CustomUserLoginSerializer

    def post(self, request):
        try:
            serializer = CustomUserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            login(request, serializer.context.get('user'))
            return Response({"message": "Login Successfully"}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=400)
