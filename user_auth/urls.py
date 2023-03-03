from django.urls import path

from user_auth import views

urlpatterns = [
    path('signup/', views.CustomUserRegistrationAPIView.as_view(), name='signup'),
    path('signup/<int:pk>', views.CustomUserRegistrationAPIView.as_view(), name='signup'),
    path('login/', views.CustomUserLoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]