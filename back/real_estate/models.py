from django.db import models
from accounts.models import User
# Create your models here.

class RealEstate(models.Model):
    region = models.TextField()
    date_time = models.TextField() # 이거 나중에 Date로 환산해줘야함
    price = models.IntegerField()
    users = models.ManyToManyField(User, related_name='real_estates', blank=True)
    def __str__(self):
        return f"{self.date_time} - {self.region} - {self.price}"
# 

