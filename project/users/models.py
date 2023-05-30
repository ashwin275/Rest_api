from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    profile = models.ImageField(upload_to='images/', null=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

