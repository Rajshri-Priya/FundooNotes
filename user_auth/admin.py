from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_auth.models import CustomUser

# Register your models here.

admin.site.register(CustomUser)
# class User(UserAdmin):
