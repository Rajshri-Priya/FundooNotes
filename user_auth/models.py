from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    address = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.username
