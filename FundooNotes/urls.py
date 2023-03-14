"""FundooNotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from FundooNotes import views

# Define the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Fundoo Notes API",
        default_version='v1',
        description="Fundoo notes api helps to create, update, delete notes.",
        # terms_of_service="https://terms/services",
        contact=openapi.Contact(email="priyagorkha711@gmail.com"),
        # license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny, ]),

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.startup),
    path('user/', include('user_auth.urls')),
    path('notes/', include('Notes.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verify_token/', TokenVerifyView.as_view(), name='token_verify'),

]

