from django.urls import path

from user_auth import views

urlpatterns = [
    path('signup/', views.CustomUserRegistrationAPIView.as_view(), name='list'),
    path('signup/<int:pk>', views.CustomUserRegistrationAPIView.as_view(), name='registeration(update/delete)'),
    path('login/', views.CustomUserLoginAPIView.as_view(), name='login'),

]