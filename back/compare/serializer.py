from rest_framework import serializers
from .models import *


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        models = Deposit
        fields = '__all__'


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        models = Saving
        fields = '__all__'
