from django.db import models
from django.conf import settings
# Create your models here.

class Deposit(models.Model):
    dcls_month = models.DateField()
    fin_co_no = models.CharField(max_length=100) 
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_cd = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=100)
    join_way = models.CharField(max_length=100)
    mtrt_int = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_member = models.TextField(blank=True, null=True)
    etc_note = models.TextField(blank=True, null=True)
    max_limit = models.IntegerField(blank=True, null=True)
    dcls_strt_day = models.CharField(max_length=100)
    dcls_end_day = models.CharField(max_length=100)
    fin_co_subm_day = models.CharField(max_length=100)

class DepositOptions(models.Model):
    deposit = models.ForeignKey(Deposit, related_name='options', on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=1)
    intr_rate_type_nm = models.CharField(max_length=2)
    sava_trm = models.CharField(max_length=3)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)

class Saving(models.Model):
    dcls_month = models.DateField()
    fin_co_no = models.CharField(max_length=100) 
    kor_co_nm = models.CharField(max_length=100)
    fin_prdt_cd = models.CharField(max_length=100)
    fin_prdt_nm = models.CharField(max_length=100)
    join_way = models.CharField(max_length=100)
    mtrt_int = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    spcl_cnd = models.TextField(blank=True, null=True)
    join_deny = models.IntegerField(blank=True, null=True)
    join_member = models.TextField(blank=True, null=True)
    etc_note = models.TextField(blank=True, null=True)
    max_limit = models.IntegerField(blank=True, null=True)
    dcls_strt_day = models.CharField(max_length=100)
    dcls_end_day = models.CharField(max_length=100)
    fin_co_subm_day = models.CharField(max_length=100)

class SavingOptions(models.Model):
    saving = models.ForeignKey(Saving, related_name='options', on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=1)
    intr_rate_type_nm = models.CharField(max_length=2)
    rsrv_type = models.CharField(max_length=1)
    rsrv_type_nm = models.CharField(max_length=5) 
    sava_trm = models.CharField(max_length=3)
    intr_rate = models.FloatField(null=True)
    intr_rate2 = models.FloatField(null=True)
