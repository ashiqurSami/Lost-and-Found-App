from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=20,blank=True)
    location=models.CharField(max_length=255,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.name} - {self.email}'