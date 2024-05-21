from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from compare.models import Deposit,Saving

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length = 50)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=300)
    profile_img = models.ImageField(upload_to='users/', default='images/user.png')
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    now_money = models.IntegerField(blank=True, null=True)  # 현재 자산
    money_per_year = models.IntegerField(blank=True, null=True)  # 연봉
    desire_amount_saving = models.IntegerField(blank=True, null=True)
    desire_amount_deposit = models.IntegerField(blank=True, null=True)
    deposit_period = models.IntegerField(blank=True, null=True)
    saving_period = models.IntegerField(blank=True, null=True)
    fav_place = models.CharField(max_length=100, blank=True, null=True)  # 선택 사항
    is_superuser = models.BooleanField(default=False)
    deposits = models.ManyToManyField(Deposit,related_name='users',blank=True)
    savings = models.ManyToManyField(Saving,related_name='user',blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','email']

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        username = data.get("username")
        nickname = data.get('nickname')
        name = data.get("name")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        profile_img = data.get("profile_img")
        age = data.get("age")
        now_money = data.get("now_money")
        money_per_year = data.get("money_per_year")
        desire_amount_saving = data.get("desire_amount_saving")
        desire_amount_deposit = data.get("desire_amount_deposit")
        deposit_period = data.get("deposit_period")
        saving_period = data.get("saving_period")
        fav_place = data.get("fav_place")

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if name:
            user_field(user, "name", name)
        if profile_img:
            user.profile_img = profile_img
        if nickname:
            user.nickname = nickname
        if age is not None:
            user.age = age
        if now_money is not None:
            user.now_money = now_money
        if money_per_year is not None:
            user.money_per_year = money_per_year
        if desire_amount_deposit is not None:
            user.desire_amount_deposit = desire_amount_deposit
        if desire_amount_saving is not None:
            user.desire_amount_saving = desire_amount_saving
        if deposit_period is not None:
            user.deposit_period = deposit_period
        if fav_place:
            user.fav_place = fav_place
        if saving_period is not None:
            user.saving_period = saving_period
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
