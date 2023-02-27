from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    address = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class UserLog(models.Model):
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.method} {self.url} {self.count}"
