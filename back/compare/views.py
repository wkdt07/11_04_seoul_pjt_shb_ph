# from collections import Counter
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from django.conf import settings
# from django.db.models import Q
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes 
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from accounts.models import User

# import requests
# from .serializer import *
# from .models import *
# from datetime import datetime
# from django.core.exceptions import ValidationError


# @api_view(['GET'])
# def make_financial_data(request):
#     BANK_API_KEY = '074e4e4a11eff3c68e5cd75a1e2b442a'
#     DEPOSIT_API_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'
#     SAVING_API_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={BANK_API_KEY}&topFinGrpNo=020000&pageNo=1'

#     deposit_res = requests.get(DEPOSIT_API_URL).json()
#     deposit_baseList = deposit_res.get('result').get('baseList')
#     deposit_optionList = deposit_res.get('result').get('optionList')

#     for base in deposit_baseList:
#         if Deposit.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')).exists():
#             continue

#         # 날짜 형식 변환 ('YYYYMM' -> 'YYYY-MM-DD')
#         dcls_month_str = base.get('dcls_month', '-1')
#         dcls_month = datetime.strptime(dcls_month_str, '%Y%m').date() if dcls_month_str != '-1' else None

#         save_product = {
#             'fin_prdt_cd': base.get('fin_prdt_cd', '-1'),
#             'fin_co_no': base.get('fin_co_no', '-1'),
#             'kor_co_nm': base.get('kor_co_nm', '-1'),
#             'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),
#             'dcls_month': dcls_month,
#             'mtrt_int': base.get('mtrt_int', '-1'),  # 그대로 문자열로 처리
#             'etc_note': base.get('etc_note', '-1'),
#             'join_deny': base.get('join_deny', -1),
#             'join_member': base.get('join_member', '-1'),
#             'join_way': base.get('join_way', '-1'),
#             'spcl_cnd': base.get('spcl_cnd', '-1'),
#             'max_limit': base.get('max_limit', -1),
#             'dcls_strt_day': base.get('dcls_strt_day', '2024-01-01') or '2024-01-01',  # 기본값 설정
#             'dcls_end_day': base.get('dcls_end_day', '2024-12-31') or '2024-12-31',  # 기본값 설정
#             'fin_co_subm_day': base.get('fin_co_subm_day', '2024-01-01') or '2024-01-01'  # 기본값 설정
#         }

#         serializer = DepositSerializer(data=save_product)
#         if serializer.is_valid(raise_exception=True):
#             product = serializer.save()

#             # 관련된 옵션 추가
#             related_options = [opt for opt in deposit_optionList if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
#             for option in related_options:
#                 save_option = {
#                     'deposit': product.id,
#                     'intr_rate_type': option.get('intr_rate_type', '0'),  # 기본값 설정
#                     'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
#                     'intr_rate': option.get('intr_rate', -1),
#                     'intr_rate2': option.get('intr_rate2', -1),
#                     'save_trm': option.get('save_trm', -1),
#                 }
#                 option_serializer = DepositOptionsSerializer(data=save_option)
#                 if option_serializer.is_valid(raise_exception=True):
#                     option_serializer.save(deposit=product)

#     saving_res = requests.get(SAVING_API_URL).json()
#     saving_baseList = saving_res.get('result').get('baseList')
#     saving_optionList = saving_res.get('result').get('optionList')

#     for base in saving_baseList:
#         if Saving.objects.filter(fin_prdt_cd=base.get('fin_prdt_cd')).exists():
#             continue

#         # 날짜 형식 변환 ('YYYYMM' -> 'YYYY-MM-DD')
#         dcls_month_str = base.get('dcls_month', '-1')
#         dcls_month = datetime.strptime(dcls_month_str, '%Y%m').date() if dcls_month_str != '-1' else None

#         save_product = {
#             'fin_prdt_cd': base.get('fin_prdt_cd', '-1'),
#             'fin_co_no': base.get('fin_co_no', '-1'),
#             'kor_co_nm': base.get('kor_co_nm', '-1'),
#             'fin_prdt_nm': base.get('fin_prdt_nm', '-1'),
#             'dcls_month': dcls_month,
#             'mtrt_int': base.get('mtrt_int', '-1'),  # 그대로 문자열로 처리
#             'etc_note': base.get('etc_note', '-1'),
#             'join_deny': base.get('join_deny', -1),
#             'join_member': base.get('join_member', '-1'),
#             'join_way': base.get('join_way', '-1'),
#             'spcl_cnd': base.get('spcl_cnd', '-1'),
#             'max_limit': base.get('max_limit', -1),
#             'dcls_strt_day': base.get('dcls_strt_day', '2024-01-01') or '2024-01-01',  # 기본값 설정
#             'dcls_end_day': base.get('dcls_end_day', '2024-12-31') or '2024-12-31',  # 기본값 설정
#             'fin_co_subm_day': base.get('fin_co_subm_day', '2024-01-01') or '2024-01-01'  # 기본값 설정
#         }

#         serializer = SavingSerializer(data=save_product)
#         if serializer.is_valid(raise_exception=True):
#             product = serializer.save()

#             # 관련된 옵션 추가
#             related_options = [opt for opt in saving_optionList if opt['fin_prdt_cd'] == base['fin_prdt_cd']]
#             for option in related_options:
#                 save_option = {
#                     'saving': product.id,
#                     'intr_rate_type': option.get('intr_rate_type', '0'),  # 기본값 설정
#                     'intr_rate_type_nm': option.get('intr_rate_type_nm', '-1'),
#                     'rsrv_type': option.get('rsrv_type', '0'),  # 기본값 설정
#                     'rsrv_type_nm': option.get('rsrv_type_nm', '-1'),
#                     'intr_rate': option.get('intr_rate', -1),
#                     'intr_rate2': option.get('intr_rate2', -1),
#                     'save_trm': option.get('save_trm', -1),
#                 }
#                 option_serializer = SavingOptionsSerializer(data=save_option)
#                 if option_serializer.is_valid(raise_exception=True):
#                     option_serializer.save(saving=product)

#     return HttpResponse("금융 데이터 생성 완료")

# @api_view(['GET']) # id 순
# def deposit_list(request):
#     deposits = Deposit.objects.all()
#     serializer = DepositSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def deposit_detail(request, fin_prdt_cd):
#     try:
#         deposit = get_object_or_404(Deposit,fin_prdt_cd=fin_prdt_cd)
#         serializer = DepositSerializer(deposit)
#         return Response(serializer.data)

#     except Exception as e:
#         return Response({"error": str(e)}, status=500) 
    

# @api_view(['GET'])
# def depositOption_list(request, fin_prdt_cd):
#     deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
#     deposit_options = DepositOptions.objects.filter(deposit=deposit)

#     if request.method == 'GET':
#         serializer = DepositOptionsSerializer(deposit_options, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def depositOption_detail(request, fin_prdt_cd, depositOption_pk):
#     deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
#     deposit_option = get_object_or_404(DepositOptions, pk=depositOption_pk, deposit=deposit)

#     if request.method == 'GET':
#         serializer = DepositOptionsSerializer(deposit_option)
#         return Response(serializer.data)
    

# @api_view(['GET']) # id 순
# def saving_list(request):
#     savings = Saving.objects.all()
#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)


# # @api_view(['GET'])
# # def saving_detail(request, saving_code):
# #     try:
# #         saving = get_object_or_404(Saving, fin_prdt_cd=saving_code)
# #         serializer = SavingSerializer(saving)
# #         users_count = saving.users.count() 
# #         data = serializer.data
# #         data['user_count'] = users_count
# #         return Response(data)
# #     except Exception as e:
# #         return Response({"error": str(e)}, status=500)

# # @api_view(['GET'])
# # def saving_detail(request, saving_code):
# #     try:
# #         print(f"Fetching saving details for code: {saving_code}")  # 추가 로그
# #         saving = get_object_or_404(Saving, fin_prdt_cd=saving_code)
# #         print(f"Found saving: {saving}")  # 추가 로그
# #         serializer = SavingSerializer(saving)
# #         users_count = saving.contract_users.count()
# #         print(f"Users count: {users_count}")  # 추가 로그
# #         data = serializer.data
# #         data['user_count'] = users_count
# #         return Response(data)
# #     except Exception as e:
# #         print(f"Error in saving_detail view: {e}")  # 추가 로그
# #         return Response({"error": str(e)}, status=500)

# @api_view(['GET'])
# def saving_detail(request, saving_code):
#     try:
#         saving = get_object_or_404(Saving, fin_prdt_cd=saving_code)
#         serializer = SavingSerializer(saving)
#         data = serializer.data  # serializer가 user_count를 포함하도록 함
#         return Response(data)
#     except Exception as e:
#         print(f"Error in saving_detail view: {e}")  # 디버깅을 위해 추가된 로그
#         return Response({"error": str(e)}, status=500)

    
# @api_view(['GET'])
# def savingOption_list(request, fin_prdt_cd):
#     saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
#     saving_options = SavingOptions.objects.filter(saving=saving)

#     if request.method == 'GET':
#         serializer = SavingOptionsSerializer(saving_options, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def savingOption_detail(request, saving_code, savingOption_pk):
#     savingOption = get_object_or_404(SavingOptions, pk=savingOption_pk)
#     if request.method == 'GET':
#         serializer = SavingOptionsSerializer(savingOption)
#         return Response(serializer.data)
    

# # 6개월~36개월
# @api_view(['GET'])
# def get_deposits(request, save_trm):
#     deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('depositoption__intr_rate')

#     serializer = DepositSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_savings(request, save_trm):
#     savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('savingoption__intr_rate')

#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_reverse_deposits(request, save_trm):
#     deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')

#     serializer = DepositSerializer(deposits, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def get_reverse_savings(request, save_trm):
#     savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')

#     serializer = SavingSerializer(savings, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'POST', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def contract_deposit(request, fin_prdt_cd):
#     deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
#     user = request.user

#     if request.method == 'GET':
#         serializer = ContractDepositSerializer(deposit)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         if user.deposits.filter(fin_prdt_cd=fin_prdt_cd).exists():
#             return Response({"detail": "이미 가입한 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         user.deposits.add(deposit)
#         user.save()
#         return Response({"detail": "예금 가입 완료"}, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         if not user.deposits.filter(fin_prdt_cd=fin_prdt_cd).exists():
#             return Response({"detail": "가입하지 않은 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         user.deposits.remove(deposit)
#         user.save()
#         return Response({"detail": "예금 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def contract_saving(request, fin_prdt_cd):
#     saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
#     user = request.user

#     if request.method == 'GET':
#         serializer = ContractSavingSerializer(saving)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         if user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
#             return Response({"detail": "이미 가입한 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         user.savings.add(saving)
#         user.save()
#         return Response({"detail": "예금 가입 완료"}, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         if not user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
#             return Response({"detail": "가입하지 않은 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
#         user.savings.remove(saving)
#         user.save()
#         return Response({"detail": "예금 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)

# # # 적금 추가하기
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # def contract_saving(request, fin_prdt_cd):
# #     saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
# #     user = request.user
# #     if user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
# #         return Response({"detail": "이미 가입한 적금입니다."}, status=status.HTTP_400_BAD_REQUEST)
# #     user.savings.add(saving)
# #     user.save()
# #     return Response({"detail": "적금 가입 완료"}, status=status.HTTP_200_OK)

# # 은행에 따라 예금 찾기
# @api_view(['GET'])
# def get_bank_deposit(request, kor_co_nm):
#     if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
#         deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
#         serializer = DepositSerializer(deposits, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)


# # # 적금 삭제하기
# # @api_view(['DELETE'])
# # @permission_classes([IsAuthenticated])
# # def contract_saving(request, fin_prdt_cd):
# #     saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
# #     user = request.user
# #     if not user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
# #         return Response({"detail": "가입하지 않은 적금입니다."}, status=status.HTTP_400_BAD_REQUEST)
# #     user.savings.remove(saving)
# #     user.save()
# #     return Response({"detail": "적금 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)


# # 은행에 따라 적금 찾기
# @api_view(['GET'])
# def get_bank_saving(request, kor_co_nm):
#     if Saving.objects.filter(kor_co_nm=kor_co_nm).exists():
#         savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
#         serializer = SavingSerializer(savings, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)


# # 추천1
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend_product_one(request):
#     user = get_object_or_404(User, username=request.user.username)
#     desired_amount_deposit = user.desire_amount_deposit
#     desired_period_deposit = user.deposit_period

#     if not desired_period_deposit or not desired_amount_deposit:
#         if not desired_period_deposit:
#             return Response({"message": "유저의 희망기간이 없습니다."})
#         elif not desired_amount_deposit:
#             return Response({"message": "유저의 희망적금금액이 없습니다."})

#     desired_period_deposit = int(desired_period_deposit)
#     desired_amount_deposit = int(desired_amount_deposit)

#     deposit = Deposit.objects.filter(
#         Q(max_limit__gte=desired_amount_deposit - desired_amount_deposit // 2) | Q(max_limit__isnull=True)
#     )

#     deposit = deposit.filter(
#         depositoption__save_trm__lte=desired_period_deposit + desired_period_deposit // 2
#     )
    
#     deposit = list(set(deposit.order_by("-depositoption__intr_rate")[:10]))

#     desired_amount_saving = user.desire_amount_saving
#     desired_period_saving = user.saving_period


#     saving = Saving.objects.filter(
#         Q(max_limit__gte=desired_amount_saving - desired_amount_saving // 2) | Q(max_limit__isnull=True)
#     )

#     saving = saving.filter(
#         savingoption__save_trm__lte=desired_period_saving + desired_period_saving // 2
#     )

#     saving = list(set(saving.order_by("-savingoption__intr_rate")[:10]))
#     # saving = saving[:10]

#     depositserializers = DepositSerializer(deposit, many=True)
#     savingserializers = SavingSerializer(saving, many=True)

#     # Create response data
#     product_list = {
#         "deposit": depositserializers.data,
#         "saving": savingserializers.data,
#     }

#     return Response(product_list)

# # 추천 2
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend_product_two(request): 
#     age = request.user.age
#     money = request.user.money
#     salary = request.user.salary
#     standard_deviation_age = 6
#     standard_deviation_money = 1000000
#     standard_deviation_salary = 1000000
#     is_not_similar_users = False

#     similar_users = User.objects.filter(
#         ~Q(username=request.user.username),
#         age__range=(age - standard_deviation_age, age + standard_deviation_age),
#         money__range=(money - standard_deviation_money, money + standard_deviation_money),
#         salary__range=(salary - standard_deviation_salary, salary + standard_deviation_salary)
#     )

#     if not similar_users.exists():
#         is_not_similar_users = True
#         similar_users = User.objects.all()

#     id_data = []


#     deposit_list = []
#     saving_list = []
    
#     for user_id in id_data:
#         user = User.objects.get(pk=user_id)
#         deposit_list.extend(user.contract_deposit.all())
#         saving_list.extend(user.contract_saving.all())

#     deposit_counter = Counter(deposit_list)
#     saving_counter = Counter(saving_list)


#     # 각 객체와 그 등장 횟수를 저장할 리스트
#     deposit_result = []
#     saving_result = []

#     for deposit, count in deposit_counter.items():
#         # Deposit 객체의 정보와 등장 횟수를 딕셔너리로 저장
#         deposit_info = {'deposit': DepositSerializer(deposit).data, 'count': count}
#         deposit_result.append(deposit_info)

#     for saving, count in saving_counter.items():
#         # Saving 객체의 정보와 등장 횟수를 딕셔너리로 저장
#         saving_info = {'saving': SavingSerializer(saving).data, 'count': count}
#         saving_result.append(saving_info)

#     # 등장 횟수를 기준으로 내림차순 정렬
#     deposit_result = sorted(deposit_result, key=lambda x: x['count'], reverse=True)[:10]
#     saving_result = sorted(saving_result, key=lambda x: x['count'], reverse=True)[:10]

#     result = {'is_not_similar_users': is_not_similar_users, 'deposit': deposit_result, 'saving': saving_result}

#     return Response(result)

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

@api_view(['GET'])
def deposit_list(request):
    deposits = Deposit.objects.all()
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_detail(request, fin_prdt_cd):
    try:
        deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
        serializer = DepositSerializer(deposit)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def depositOption_list(request, fin_prdt_cd):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    deposit_options = DepositOptions.objects.filter(deposit=deposit)
    if request.method == 'GET':
        serializer = DepositOptionsSerializer(deposit_options, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def depositOption_detail(request, fin_prdt_cd, depositOption_pk):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    deposit_option = get_object_or_404(DepositOptions, pk=depositOption_pk, deposit=deposit)
    if request.method == 'GET':
        serializer = DepositOptionsSerializer(deposit_option)
        return Response(serializer.data)

@api_view(['GET'])
def saving_list(request):
    savings = Saving.objects.all()
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_detail(request, saving_code):
    try:
        saving = get_object_or_404(Saving, fin_prdt_cd=saving_code)
        serializer = SavingSerializer(saving)
        data = serializer.data
        return Response(data)
    except Exception as e:
        print(f"Error in saving_detail view: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def savingOption_list(request, fin_prdt_cd):
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    saving_options = SavingOptions.objects.filter(saving=saving)
    if request.method == 'GET':
        serializer = SavingOptionsSerializer(saving_options, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def savingOption_detail(request, saving_code, savingOption_pk):
    savingOption = get_object_or_404(SavingOptions, pk=savingOption_pk)
    if request.method == 'GET':
        serializer = SavingOptionsSerializer(savingOption)
        return Response(serializer.data)

@api_view(['GET'])
def get_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('depositoption__intr_rate')
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('savingoption__intr_rate')
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_reverse_deposits(request, save_trm):
    deposits = Deposit.objects.filter(depositoption__save_trm=save_trm).order_by('-depositoption__intr_rate')
    serializer = DepositSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_reverse_savings(request, save_trm):
    savings = Saving.objects.filter(savingoption__save_trm=save_trm).order_by('-savingoption__intr_rate')
    serializer = SavingSerializer(savings, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def contract_deposit(request, fin_prdt_cd):
    deposit = get_object_or_404(Deposit, fin_prdt_cd=fin_prdt_cd)
    user = request.user
    if request.method == 'GET':
        serializer = ContractDepositSerializer(deposit)
        return Response(serializer.data)
    elif request.method == 'POST':
        if user.deposits.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response({"detail": "이미 가입한 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.deposits.add(deposit)
        user.save()
        return Response({"detail": "예금 가입 완료"}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if not user.deposits.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response({"detail": "가입하지 않은 예금입니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.deposits.remove(deposit)
        user.save()
        return Response({"detail": "예금 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def contract_saving(request, fin_prdt_cd):
    saving = get_object_or_404(Saving, fin_prdt_cd=fin_prdt_cd)
    user = request.user
    if request.method == 'GET':
        serializer = ContractSavingSerializer(saving)
        return Response(serializer.data)
    elif request.method == 'POST':
        if user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response({"detail": "이미 가입한 적금입니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.savings.add(saving)
        user.save()
        return Response({"detail": "적금 가입 완료"}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if not user.savings.filter(fin_prdt_cd=fin_prdt_cd).exists():
            return Response({"detail": "가입하지 않은 적금입니다."}, status=status.HTTP_400_BAD_REQUEST)
        user.savings.remove(saving)
        user.save()
        return Response({"detail": "적금 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_bank_deposit(request, kor_co_nm):
    if Deposit.objects.filter(kor_co_nm=kor_co_nm).exists():
        deposits = Deposit.objects.filter(kor_co_nm=kor_co_nm)
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_bank_saving(request, kor_co_nm):
    if Saving.objects.filter(kor_co_nm=kor_co_nm).exists():
        savings = Saving.objects.filter(kor_co_nm=kor_co_nm)
        serializer = SavingSerializer(savings, many=True)
        return Response(serializer.data)
    else:
        return Response({ "detail": "해당은행의 상품이 없습니다.." }, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_product_one(request):
    user = get_object_or_404(User, username=request.user.username)
    desired_amount_deposit = user.desire_amount_deposit
    desired_period_deposit = user.deposit_period
    if not desired_period_deposit or not desired_amount_deposit:
        if not desired_period_deposit:
            return Response({"message": "유저의 희망기간이 없습니다."})
        elif not desired_amount_deposit:
            return Response({"message": "유저의 희망적금금액이 없습니다."})
    desired_period_deposit = int(desired_period_deposit)
    desired_amount_deposit = int(desired_amount_deposit)
    deposit = Deposit.objects.filter(
        Q(max_limit__gte=desired_amount_deposit - desired_amount_deposit // 2) | Q(max_limit__isnull=True)
    )
    deposit = deposit.filter(
        depositoption__save_trm__lte=desired_period_deposit + desired_period_deposit // 2
    )
    deposit = list(set(deposit.order_by("-depositoption__intr_rate")[:10]))
    desired_amount_saving = user.desire_amount_saving
    desired_period_saving = user.saving_period
    saving = Saving.objects.filter(
        Q(max_limit__gte=desired_amount_saving - desired_amount_saving // 2) | Q(max_limit__isnull=True)
    )
    saving = saving.filter(
        savingoption__save_trm__lte=desired_period_saving + desired_period_saving // 2
    )
    saving = list(set(saving.order_by("-savingoption__intr_rate")[:10]))
    depositserializers = DepositSerializer(deposit, many=True)
    savingserializers = SavingSerializer(saving, many=True)
    product_list = {
        "deposit": depositserializers.data,
        "saving": savingserializers.data,
    }
    return Response(product_list)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_product_two(request):
    age = request.user.age
    money = request.user.money
    salary = request.user.salary
    standard_deviation_age = 6
    standard_deviation_money = 1000000
    standard_deviation_salary = 1000000
    is_not_similar_users = False
    similar_users = User.objects.filter(
        ~Q(username=request.user.username),
        age__range=(age - standard_deviation_age, age + standard_deviation_age),
        money__range=(money - standard_deviation_money, money + standard_deviation_money),
        salary__range=(salary - standard_deviation_salary, salary + standard_deviation_salary)
    )
    if not similar_users.exists():
        is_not_similar_users = True
        similar_users = User.objects.all()
    id_data = []
    deposit_list = []
    saving_list = []
    for user_id in id_data:
        user = User.objects.get(pk=user_id)
        deposit_list.extend(user.contract_deposit.all())
        saving_list.extend(user.contract_saving.all())
    deposit_counter = Counter(deposit_list)
    saving_counter = Counter(saving_list)
    deposit_result = []
    saving_result = []
    for deposit, count in deposit_counter.items():
        deposit_info = {'deposit': DepositSerializer(deposit).data, 'count': count}
        deposit_result.append(deposit_info)
    for saving, count in saving_counter.items():
        saving_info = {'saving': SavingSerializer(saving).data, 'count': count}
        saving_result.append(saving_info)
    deposit_result = sorted(deposit_result, key=lambda x: x['count'], reverse=True)[:10]
    saving_result = sorted(saving_result, key=lambda x: x['count'], reverse=True)[:10]
    result = {'is_not_similar_users': is_not_similar_users, 'deposit': deposit_result, 'saving': saving_result}
    return Response(result)