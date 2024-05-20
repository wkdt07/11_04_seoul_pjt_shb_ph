# # from rest_framework import serializers
# # from .models import *

# # class DepositOptionsSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = DepositOptions
# #         fields = '__all__'
# #         read_only_fields = ('deposit',)

# # class DepositOptionsSerializer1(serializers.ModelSerializer):
# #     class DepositSerializer(serializers.ModelSerializer):
# #         class Meta:
# #             model = Deposit
# #             fields = '__all__'
# #     deposit = DepositSerializer()
# #     class Meta:
# #         model = DepositOptions
# #         fields = '__all__'


# # class DepositSerializer(serializers.ModelSerializer):
# #     depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
# #     depositoption2_set = DepositOptionsSerializer1(many=True, read_only=True)
# #     options = DepositOptionsSerializer(many=True, read_only=True, source='depositoptions_set')
    
# #     class Meta:
# #         model = Deposit
# #         fields = '__all__'
# #         read_only_fields = ('contract_user',)       

# # class ContractDepositSerializer(serializers.ModelSerializer):
# #     depositoption_set = DepositOptionsSerializer(many=True, read_only=True)
# #     class Meta:
# #         model = Deposit
# #         fields = ('deposit_code','name', 'kor_co_nm', 'depositoption_set')


# # class SavingOptionsSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = SavingOptions
# #         fields = '__all__'
# #         read_only_fields = ('saving',)

# # class SavingOptionsSerializer1(serializers.ModelSerializer):
# #     class SavingSerializer(serializers.ModelSerializer):
# #         class Meta:
# #             model = Saving
# #             fields = '__all__'
# #     saving = SavingSerializer()
# #     class Meta:
# #         model = SavingOptions
# #         fields = '__all__'

# # class SavingSerializer(serializers.ModelSerializer):
# #     savingoption_set = SavingOptionsSerializer(many=True, read_only=True)
# #     options = DepositOptionsSerializer(many=True, read_only=True, source='depositoptions_set')

# #     class Meta:
# #         model = Saving
# #         fields = '__all__'
# #         read_only_fields = ('contract_user',)


# # class ContractSavingSerializer(serializers.ModelSerializer):
# #     savingoption_set = SavingOptionsSerializer(many=True, read_only=True)
# #     class Meta:
# #         model = Saving
# #         fields = ('saving_code','name','kor_co_nm', 'savingoption_set')


# # serializers.py

# from rest_framework import serializers
# from .models import *
# from django.contrib.auth import get_user_model

# User = get_user_model()
# class DepositOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DepositOptions
#         fields = '__all__'
#         read_only_fields = ('deposit',)

# class DepositOptionsSerializer1(serializers.ModelSerializer):
#     class DepositSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Deposit
#             fields = '__all__'
#     deposit = DepositSerializer()
#     class Meta:
#         model = DepositOptions
#         fields = '__all__'


# class DepositSerializer(serializers.ModelSerializer):
#     options = DepositOptionsSerializer(many=True, read_only=True)

#     class Meta:
#         model = Deposit
#         fields = '__all__'
#         read_only_fields = ('contract_user',)       

# class ContractDepositSerializer(serializers.ModelSerializer):
#     options = DepositOptionsSerializer(many=True, read_only=True)
#     class Meta:
#         model = Deposit
#         fields = ('deposit_code','fin_prdt_nm', 'kor_co_nm', 'options')


# class SavingOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavingOptions
#         fields = '__all__'
#         read_only_fields = ('saving',)

# class SavingOptionsSerializer1(serializers.ModelSerializer):
#     class SavingSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Saving
#             fields = '__all__'
#     saving = SavingSerializer()
#     class Meta:
#         model = SavingOptions
#         fields = '__all__'

# class SavingSerializer(serializers.ModelSerializer):
#     options = SavingOptionsSerializer(many=True, read_only=True)

#     class Meta:
#         model = Saving
#         fields = '__all__'
#         read_only_fields = ('contract_user',)


# class ContractSavingSerializer(serializers.ModelSerializer):
#     options = SavingOptionsSerializer(many=True, read_only=True)
#     class Meta:
#         model = Saving
#         fields = ('saving_code','fin_prdt_nm','kor_co_nm', 'options')
        
        
# class UserSerializer(serializers.ModelSerializer):
#     deposits = DepositSerializer(many=True, read_only=True)
#     savings = SavingSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'deposits', 'savings')

from rest_framework import serializers
from .models import Deposit, DepositOptions, Saving, SavingOptions

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('deposit',)

class DepositSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('contract_users',)  # 사용자가 예금에 대해 ManyToManyField로 연결됨
    def get_user_count(self,obj):
        return obj.users.count()

class ContractDepositSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Deposit
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'options')

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('saving',)

class SavingSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('contract_users',)  # 사용자가 적금에 대해 ManyToManyField로 연결됨
    def get_user_count(self,obj):
        return obj.users.count()

class ContractSavingSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = Saving
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'options')
