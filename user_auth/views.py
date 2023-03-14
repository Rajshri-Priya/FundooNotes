import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from logging_confiq.logger import get_logger
from user_auth.models import CustomUser
from user_auth.serializers import CustomUserRegistrationSerializer, CustomUserLoginSerializer
from django.views.generic import View

# logging config
logger = get_logger()


# Create your views here.

class CustomUserRegistrationAPIView(APIView):
    """
         Class is to register for the user
    """
    serializer_class = CustomUserRegistrationSerializer

    @swagger_auto_schema(request_body=CustomUserRegistrationSerializer, operation_summary='POST User Registeration')
    def post(self, request):
        try:
            serializer = CustomUserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # return render(request, "user_auth/registration_success.html", {"user": serializer.data})

            return Response({"success": True, "message": "user Registered Successfully", "data": serializer.data,
                             "status": 201}, status=201)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            user = request.user
            serializer = CustomUserRegistrationSerializer(user)
            return Response({"success": True, 'message': 'user Retrieve successfully!', 'Data': serializer.data,
                             "status": 200}, status=200)
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
    """
        This class is used for the User login
    """
    serializer_class = CustomUserLoginSerializer

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CustomUserLoginSerializer, operation_summary='POST User Login')
    def post(self, request):
        try:
            serializer = CustomUserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.context.get('user')
            login(request, user)
            return Response({"success": True, "message": "Login Successfully", "user": user, "status": 201},
                            status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 401}, status=401)


class LogoutView(APIView):
    """
        This class is used for the User logout
    """

    def get(self, request):
        try:
            # Check if user is authenticated
            if request.user.is_authenticated:
                # Logout user
                logout(request)
                # Redirect to login page
                return Response({'message': 'logout successfully.'})
            else:
                return Response({'message': 'You are not logged in.'})
        except Exception as e:
            logger.exception(e)
            return Response({'message': 'An error occurred during logout: {}'.format(str(e))})


class LoginView(View):
    def get(self, request):
        return render(request, "user_auth/login.html")

    def post(self, request):
        api_url = 'http://127.0.0.1:8000/user/login/'
        data = {'username': request.POST['username'], 'password': request.POST['password']}
        response = requests.post(api_url, data=data)
        print(dir(response))
        # Check the response status code and render the appropriate template
        if response.status_code == 201:
            response_data = response.json()
            user = response_data.get('user', '')
            # context = {'data': user}
            return render(request, ["user_auth/login_success.html", "user_auth/home.html"], {"user": user})
            # return redirect('base.html')
        else:
            return render(request, "user_auth/login_failure.html")


class RegistrationView(View):
    def get(self, request):
        return render(request, "user_auth/registeration.html")

    def post(self, request):
        # Make a POST request to the API endpoint with the form data
        api_url = 'http://127.0.0.1:8000/user/signup/'
        data = {'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'],
                'address': request.POST['address'], 'phone': request.POST['phone'], 'email': request.POST['email'],
                'username': request.POST['username'], 'password': request.POST.get('password')
                }

        response = requests.post(api_url, data=data)
        # Check the response status code and render the appropriate template
        if response.status_code == 201:
            return render(request, 'user_auth/register_success.html')
        else:
            response_data = response.json()
            message = response_data.get('message', '')
            return render(request, 'user_auth/register_failure.html', {'message': message})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(request):
        # return render(request, "user_auth/profile.html")
        api_url = 'http://127.0.0.1:8000/user/signup/'
        response = requests.get(api_url)
        # Check the response status code and render the appropriate template
        if response.status_code == 201:
            response_data = response.json()
            print(response_data)
            return render(request, 'user_auth/profile.html')


class Logout(View):
    def get(self, request):
        return render(request, 'user_auth/logout.html')


def base_page(request):
    return render(request, 'user_auth/base.html')


def home_page(request):
    return render(request, 'user_auth/home.html')
