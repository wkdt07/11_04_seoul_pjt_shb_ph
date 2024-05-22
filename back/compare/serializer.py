

# from rest_framework import serializers
# from .models import Deposit, DepositOptions, Saving, SavingOptions

# class DepositOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DepositOptions
#         fields = '__all__'
#         read_only_fields = ('deposit',)

# class DepositSerializer(serializers.ModelSerializer):
#     options = DepositOptionsSerializer(many=True, read_only=True)

#     class Meta:
#         model = Deposit
#         fields = '__all__'
#         read_only_fields = ('contract_users',)  # 사용자가 예금에 대해 ManyToManyField로 연결됨
#     def get_user_count(self,obj):
#         return obj.users.count()

# class ContractDepositSerializer(serializers.ModelSerializer):
#     options = DepositOptionsSerializer(many=True, read_only=True)
#     class Meta:
#         model = Deposit
#         fields = ('fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'options')

# class SavingOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SavingOptions
#         fields = '__all__'
#         read_only_fields = ('saving',)

# class SavingSerializer(serializers.ModelSerializer):
#     options = SavingOptionsSerializer(many=True, read_only=True)

#     class Meta:
#         model = Saving
#         fields = '__all__'
#         read_only_fields = ('contract_users',)  # 사용자가 적금에 대해 ManyToManyField로 연결됨
#     def get_user_count(self,obj):
#         return obj.users.count()


# class ContractSavingSerializer(serializers.ModelSerializer):
#     options = SavingOptionsSerializer(many=True, read_only=True)
#     class Meta:
#         model = Saving
#         fields = ('fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'options')


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

    def get_user_count(self, obj):
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

    def get_user_count(self, obj):
        return obj.users.count()

class ContractSavingSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'options')
