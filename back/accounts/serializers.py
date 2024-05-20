# from rest_framework import serializers

# from dj_rest_auth.registration.serializers import RegisterSerializer

# from .models import User

# class CustomRegisterSerializer(RegisterSerializer):
#     nickname = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         max_length = 255,
#     )

#     def get_cleaned_data(self):
#         return {
#             'username':self.validated_data.get('username',''),
#             'password1': self.validated_data.get('password1', ''),
#             # nickname 필드 추가
#             'nickname': self.validated_data.get('nickname', ''),
#         }
# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# class CustomUserDetailsSerializer(UserDetailsSerializer):
#     class Meta:
#         extra_fields = []
#         # see https://github.com/iMerica/dj-rest-auth/issues/181
#         # UserModel.XYZ causing attribute error while importing other
#         # classes from `serializers.py`. So, we need to check whether the auth model has
#         # the attribute or not
#         if hasattr(UserModel, 'USERNAME_FIELD'):
#             extra_fields.append(UserModel.USERNAME_FIELD)
#         if hasattr(UserModel, 'EMAIL_FIELD'):
#             extra_fields.append(UserModel.EMAIL_FIELD)
#         if hasattr(UserModel, 'first_name'):
#             extra_fields.append('first_name')
#         if hasattr(UserModel, 'last_name'):
#             extra_fields.append('last_name')
#         if hasattr(UserModel, 'nickname'):
#             extra_fields.append('nickname')
#         model = UserModel
#         fields = ('pk', *extra_fields)
#         read_only_fields = ('email',)
# serializers.py
# from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from .models import User

# class CustomRegisterSerializer(RegisterSerializer):
#     email = serializers.EmailField(required=False, allow_blank=True)  # email 필드를 선택적으로 설정
#     nickname = serializers.CharField(required=False, allow_blank=True, max_length=255)
#     now_money = serializers.IntegerField()
#     money_per_year = serializers.IntegerField()
#     fav_place = serializers.CharField(max_length=100, required=False)

#     def get_cleaned_data(self):
#         cleaned_data = super().get_cleaned_data()
#         cleaned_data['email'] = self.validated_data.get('email', '')
#         cleaned_data['nickname'] = self.validated_data.get('nickname', '')
#         return cleaned_data

#     def save(self, request):
#         user = super().save(request)
#         user.email = self.cleaned_data.get('email', '')
#         user.nickname = self.cleaned_data.get('nickname', '')
#         user.save()
#         return user



# serializers.py
# from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from .models import User

# class CustomRegisterSerializer(RegisterSerializer):
#     email = serializers.EmailField(required=False, allow_blank=True)  # email 필드를 선택적으로 설정
#     nickname = serializers.CharField(required=False, allow_blank=True, max_length=255)
#     age = serializers.IntegerField()
#     now_money = serializers.IntegerField()
#     money_per_year = serializers.IntegerField()
#     fav_place = serializers.CharField(max_length=100, required=False)

#     def get_cleaned_data(self):
#         cleaned_data = super().get_cleaned_data()
#         cleaned_data['email'] = self.validated_data.get('email', '')
#         cleaned_data['nickname'] = self.validated_data.get('nickname', '')
#         cleaned_data['age'] = self.validated_data.get('age', 0)
#         cleaned_data['now_money'] = self.validated_data.get('now_money', 0)
#         cleaned_data['money_per_year'] = self.validated_data.get('money_per_year', 0)
#         cleaned_data['fav_place'] = self.validated_data.get('fav_place', '')
#         return cleaned_data

#     def save(self, request):
#         user = super().save(request)
#         user.email = self.cleaned_data.get('email', '')
#         user.nickname = self.cleaned_data.get('nickname', '')
#         user.age = self.cleaned_data.get('age', 0)
#         user.now_money = self.cleaned_data.get('now_money', 0)
#         user.money_per_year = self.cleaned_data.get('money_per_year', 0)
#         user.fav_place = self.cleaned_data.get('fav_place', '')
#         user.save()
#         return user

# from rest_framework import serializers
# from allauth.account.adapter import get_adapter
# from .models import User
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from compare.serializer import ContractDepositSerializer, ContractSavingSerializer

# class CustomRegisterSerializer(RegisterSerializer):
#     username = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         max_length=100
#     )
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField(required=False)
#     age = serializers.IntegerField()
#     now_money = serializers.IntegerField()
#     money_per_year = serializers.IntegerField()
#     fav_place = serializers.CharField(max_length=100, required=False)

#     def get_cleaned_data(self):
#         cleaned_data = super().get_cleaned_data()
#         cleaned_data['username'] = self.validated_data.get('username', '')
#         cleaned_data['password1'] = self.validated_data.get('password1', '')
#         cleaned_data['password2'] = self.validated_data.get('password2', '')
#         cleaned_data['name'] = self.validated_data.get('name', '')
#         cleaned_data['email'] = self.validated_data.get('email', '')
#         cleaned_data['age'] = self.validated_data.get('age', 0)
#         cleaned_data['now_money'] = self.validated_data.get('now_money', 0)
#         cleaned_data['money_per_year'] = self.validated_data.get('money_per_year', 0)
#         cleaned_data['fav_place'] = self.validated_data.get('fav_place', '')
#         return cleaned_data

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         self.custom_signup(request, user)
#         return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('profile_img', 'id', 'username', 'name', 'email', 'age', 'now_money', 'money_per_year','fav_place')
#         read_only_fields = ('id', 'username', 'name',)

# class UserInfoSerializer(serializers.ModelSerializer):
#     profile_img = serializers.ImageField(use_url=True)
#     contract_deposit = ContractDepositSerializer(many=True)
#     contract_saving = ContractSavingSerializer(many=True)

#     class Meta:
#         model = User
#         fields = '__all__'
#         read_only_fields = ('id', 'username', 'name',)


from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from compare.serializer import ContractDepositSerializer, ContractSavingSerializer

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True, max_length=100)
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=False, allow_blank=True)  # 선택 사항
    age = serializers.IntegerField(required=True)
    now_money = serializers.IntegerField(required=True)
    money_per_year = serializers.IntegerField(required=True)
    fav_place = serializers.CharField(max_length=100, required=False, allow_blank=True)  # 선택 사항

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['username'] = self.validated_data.get('username', '')
        cleaned_data['password1'] = self.validated_data.get('password1', '')
        cleaned_data['password2'] = self.validated_data.get('password2', '')
        cleaned_data['name'] = self.validated_data.get('name', '')
        cleaned_data['email'] = self.validated_data.get('email', '')
        cleaned_data['age'] = self.validated_data.get('age', 0)
        cleaned_data['now_money'] = self.validated_data.get('now_money', 0)
        cleaned_data['money_per_year'] = self.validated_data.get('money_per_year', 0)
        cleaned_data['fav_place'] = self.validated_data.get('fav_place', '')
        return cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
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
            'fav_place', 'is_superuser', 'contract_deposit', 'contract_saving'
        ]
        read_only_fields = ['id', 'username', 'is_superuser']