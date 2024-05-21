from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from compare.serializer import ContractDepositSerializer, ContractSavingSerializer

class UserInfoSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True)
    contract_deposit = ContractDepositSerializer(many=True, read_only=True)
    contract_saving = ContractSavingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
           'id', 'username', 'nickname','name', 'email', 'profile_img', 'financial_products', 
            'age', 'now_money', 'money_per_year', 'desire_amount_saving', 
            'desire_amount_deposit', 'deposit_period', 'saving_period', 
            'fav_place', 'is_superuser', 'contract_deposit', 'contract_saving'
        ]
        read_only_fields = ['id', 'username', 'is_superuser']



class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True, max_length=100)
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    age = serializers.IntegerField(required=True)
    now_money = serializers.IntegerField(required=True)
    money_per_year = serializers.IntegerField(required=True)
    profile_img = serializers.ImageField(required=False, use_url=True)
    fav_place = serializers.CharField(max_length=100, required=False, allow_blank=True)
    nickname = serializers.CharField(required=True, max_length=100)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['username'] = self.validated_data.get('username', '')
        cleaned_data['password1'] = self.validated_data.get('password1', '')
        cleaned_data['password2'] = self.validated_data.get('password2', '')
        cleaned_data['name'] = self.validated_data.get('name', '')
        cleaned_data['email'] = self.validated_data.get('email', '')
        cleaned_data['age'] = int(self.validated_data.get('age', 0))
        cleaned_data['now_money'] = int(self.validated_data.get('now_money', 0))
        cleaned_data['money_per_year'] = int(self.validated_data.get('money_per_year', 0))
        cleaned_data['profile_img'] = self.validated_data.get('profile_img', None)
        cleaned_data['fav_place'] = self.validated_data.get('fav_place', '')
        cleaned_data['nickname'] = self.validated_data.get('nickname', '')
        return cleaned_data

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)

        # 프로필 이미지가 없을 때 기본 이미지 설정
        if not user.profile_img:
            user.profile_img = 'images/user.png'
            user.save()
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'profile_img', 'financial_products', 
            'age', 'now_money', 'money_per_year', 'desire_amount_saving', 
            'desire_amount_deposit', 'deposit_period', 'saving_period', 
            'fav_place', 'nickname'
        ]

    def save(self, **kwargs):
        user = super().save(**kwargs)
        if not user.profile_img:
            user.profile_img = 'image/user.png'
            user.save()
        return user
    
    
class UserInfoSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True)
    contract_deposit = ContractDepositSerializer(many=True, read_only=True)
    contract_saving = ContractSavingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'email', 'profile_img', 'financial_products', 
            'age', 'now_money', 'money_per_year', 'desire_amount_saving', 
            'desire_amount_deposit', 'deposit_period', 'saving_period', 
            'fav_place', 'is_superuser', 'contract_deposit', 'contract_saving','nickname',
        ]
        read_only_fields = ['id', 'username', 'is_superuser']
        
# class UserProfileSerializer(serializers.ModelSerializer):
#     profile_img = serializers.ImageField(use_url=True, required=False)

#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'name', 'email', 'profile_img', 'age', 
#             'now_money', 'money_per_year', 'fav_place', 'nickname'
#         ]
#         read_only_fields = ['id', 'username']