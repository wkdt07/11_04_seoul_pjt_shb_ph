from accounts.models import User
from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
import requests
from .serializer import *
from models import *




def make_financial_data(request):
    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={settings.BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
    deposit_res = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_res.get('result').get('baseList')
    deposit_optionList = deposit_res.get('result').get('optionList')

    for base in deposit_baseList:
        if Deposit.objects.filter(deposit_code=base.get('fin_prdt_cd')):
            continue
        save_product = {
            'deposit_code': base.get('fin_prdt_cd', '-1'),
            'fin_co_no': base.get('fin_co_no', '-1'),
            'kor_co_nm': base.get('kor_co_nm', '-1'),
            'name': base.get('fin_prdt_nm', '-1'),
            'dcls_month': base.get('dcls_month', '-1'),
            'mtrt_int': base.get('mtrt_int', '-1'),
            'etc_note': base.get('etc_note', '-1'),
            'join_deny': base.get('join_deny', -1),
            'join_member': base.get('join_member', '-1'),
            'join_way': base.get('join_way', '-1'),
            'spcl_cnd': base.get('spcl_cnd', '-1'),
            'max_limit': base.get('max_limit', -1),
        }
        serializer = DepositSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()    


# Create your views here.

@api_view(['GET'])
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def depositOptions_list(request, deposit_code):
    deposit = get_object_or_404(Deposit, deposit_code=deposit_code)
    deposit_options = DepositOptions.objects.filter(deposit=deposit)

    if request.method == 'GET':
        serializer = DepositOptionsSerializer(deposit_options, many=True)
        return Response(serializer.data)


