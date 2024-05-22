from django.db import models
from accounts.models import User
# Create your models here.

class RealEstate(models.Model):
    pass
    user= models.ForeignKey(User)
    