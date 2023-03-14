from django.urls import path

from user_auth import views

urlpatterns = [
    path('signup/', views.CustomUserRegistrationAPIView.as_view(), name='signup'),
    path('signup/<int:pk>', views.CustomUserRegistrationAPIView.as_view(), name='signup'),
    path('login/', views.CustomUserLoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout_view/', views.Logout.as_view(), name='logout_render'),
    path('login_view/', views.LoginView.as_view(), name='login_render'),
    path('register_view/', views.RegistrationView.as_view(), name='register_render'),
    path('base/', views.base_page, name='base'),
    path('home/', views.home_page, name='home'),
    path('profile/', views.LoginView.as_view, name='profile')
]
