from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_auth.models import CustomUser,UserLog

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserLog)
# class User(UserAdmin):
