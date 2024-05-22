from django.shortcuts import render

# Create your views here.
from collections import Counter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User

import requests
from .serializer import *
from .models import *
from datetime import datetime
from django.core.exceptions import ValidationError


def make_data(request):
    pass

@api_view(['GET'])
def make_financial_data(request):
    BANK_API_KEY = '074e4e4a11eff3c68e5cd75a1e2b442a'
    DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
    SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'

    deposit_res = requests.get(DEPOSIT_API_URL).json()
    deposit_baseList = deposit_res.get('result').get('baseList')
    deposit_optionList = deposit_res.get('result').get('optionList')

    for base in deposit_baseList:
        if Deposit.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')).exists():
            continue

        # 날짜 형식 변환 ('YYYYMM' -> 'YYYY-MM-DD')
        dcls_month_str = base.get('dcls_month', '-1')
        dcls_month = datetime.strptime(dcls_month_str, '%Y%m').date() if dcls_month_str != '-1' else None

        save_product = {
            'fin_prdt_cd': base.get('fin_prdt_cd', '-1'),
            'fin_co_no': base.get('fin_co_no', '-1'),
            'kor_co_nm': base.get('kor_co_nm', '-1'),
            'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),
            'dcls_month': dcls_month,
            'mtrt_int': base.get('mtrt_int', '-1'),  # 그대로 문자열로 처리
            'etc_note': base.get('etc_note', '-1'),
            'join_deny': base.get('join_deny', -1),
            'join_member': base.get('join_member', '-1'),
            'join_way': base.get('join_way', '-1'),
            'spcl_cnd': base.get('spcl_cnd', '-1'),
            'max_limit': base.get('max_limit', -1),
            'dcls_strt_day': base.get('dcls_strt_day', '2024-01-01') or '2024-01-01',  # 기본값 설정
            'dcls_end_day': base.get('dcls_end_day', '2024-12-31') or '2024-12-31',  # 기본값 설정
            'fin_co_subm_day': base.get('fin_co_subm_day', '2024-01-01') or '2024-01-01'  # 기본값 설정
        }

        serializer = DepositSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()

            # 관련된 옵션 추가
            related_options = [opt for opt in deposit_optionList if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            for option in related_options:
                save_option = {
                    'deposit': product.id,
                    'intr_rate_type': option.get('intr_rate_type', '0'),  # 기본값 설정
                    'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
                    'intr_rate': option.get('intr_rate', -1),
                    'intr_rate2': option.get('intr_rate2', -1),
                    'save_trm': option.get('save_trm', -1),
                }
                option_serializer = DepositOptionsSerializer(data=save_option)
                if option_serializer.is_valid(raise_exception=True):
                    option_serializer.save(deposit=product)

    saving_res = requests.get(SAVING_API_URL).json()
    saving_baseList = saving_res.get('result').get('baseList')
    saving_optionList = saving_res.get('result').get('optionList')

    for base in saving_baseList:
        if Saving.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')).exists():
            continue

        # 날짜 형식 변환 ('YYYYMM' -> 'YYYY-MM-DD')
        dcls_month_str = base.get('dcls_month', '-1')
        dcls_month = datetime.strptime(dcls_month_str, '%Y%m').date() if dcls_month_str != '-1' else None

        save_product = {
            'fin_prdt_cd': base.get('fin_prdt_cd', '-1'),
            'fin_co_no': base.get('fin_co_no', '-1'),
            'kor_co_nm': base.get('kor_co_nm', '-1'),
            'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),
            'dcls_month': dcls_month,
            'mtrt_int': base.get('mtrt_int', '-1'),  # 그대로 문자열로 처리
            'etc_note': base.get('etc_note', '-1'),
            'join_deny': base.get('join_deny', -1),
            'join_member': base.get('join_member', '-1'),
            'join_way': base.get('join_way', '-1'),
            'spcl_cnd': base.get('spcl_cnd', '-1'),
            'max_limit': base.get('max_limit', -1),
            'dcls_strt_day': base.get('dcls_strt_day', '2024-01-01') or '2024-01-01',  # 기본값 설정
            'dcls_end_day': base.get('dcls_end_day', '2024-12-31') or '2024-12-31',  # 기본값 설정
            'fin_co_subm_day': base.get('fin_co_subm_day', '2024-01-01') or '2024-01-01'  # 기본값 설정
        }

        serializer = SavingSerializer(data=save_product)
        if serializer.is_valid(raise_exception=True):
            product = serializer.save()

            # 관련된 옵션 추가
            related_options = [opt for opt in saving_optionList if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
            for option in related_options:
                save_option = {
                    'saving': product.id,
                    'intr_rate_type': option.get('intr_rate_type', '0'),  # 기본값 설정
                    'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
                    'rsrv_type': option.get('rsrv_type', '0'),  # 기본값 설정
                    'rsrv_type_nm': option.get('rsrv_type_nm', '-1'),
                    'intr_rate': option.get('intr_rate', -1),
                    'intr_rate2': option.get('intr_rate2', -1),
                    'save_trm': option.get('save_trm', -1),
                }
                option_serializer = SavingOptionsSerializer(data=save_option)
                if option_serializer.is_valid(raise_exception=True):
                    option_serializer.save(saving=product)

    return HttpResponse("금융 데이터 생성 완료")
