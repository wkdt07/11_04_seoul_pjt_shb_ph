from rest_framework import serializers
from .models import *

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('deposit',)

class DepositOptionsSerializer1(serializers.ModelSerializer):
    class DepositSerializer(serializers.ModelSerializer):
        class Meta:
            model = Deposit
            fields = '__all__'
    deposit = DepositSerializer()
    class Meta:
        model = DepositOptions
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
    depositoption2_set = DepositOptionsSerializer1(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('contract_user',)       

class ContractDepositSerializer(serializers.ModelSerializer):
    depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = ('deposit_code','name', 'kor_co_nm', 'depositoption_set')


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('saving',)

class SavingOptionsSerializer1(serializers.ModelSerializer):
    class SavingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Saving
            fields = '__all__'
    saving = SavingSerializer()
    class Meta:
        model = SavingOptions
        fields = '__all__'

class SavingSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('contract_user',)


class ContractSavingSerializer(serializers.ModelSerializer):
    savingoption_set = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Saving
        fields = ('saving_code','name','kor_co_nm', 'savingoption_set')