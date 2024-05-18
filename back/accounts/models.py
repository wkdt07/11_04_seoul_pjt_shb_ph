from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
# Create your models here.

class User(AbstractUser):
  nickname=models.CharField(max_length=100)
