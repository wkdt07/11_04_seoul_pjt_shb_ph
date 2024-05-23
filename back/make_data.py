# import os
# import django
# import random
# import requests
# import json
# from collections import OrderedDict

# # Django 환경 설정 로드
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pjt.settings')  # 'django_pjt'는 실제 프로젝트 이름으로 대체
# django.setup()

# from compare.models import Deposit, Saving

# # 샘플 데이터
# first_name_samples = '김이박최정강조윤장임'
# middle_name_samples = '민서예지도하주윤채현지'
# last_name_samples = '준윤우원호후서연아은진'

# # 랜덤 이름 생성 함수
# def random_name():
#     result = ''
#     result += random.choice(first_name_samples)
#     result += random.choice(middle_name_samples)
#     result += random.choice(last_name_samples)
#     return result + str(random.randint(1, 100))

# # 현재 API에 들어있는 금융 상품 코드 리스트 저장
# DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
# SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
# API_KEY = '074e4e4a11eff3c68e5cd75a1e2b442a'

# financial_products = []
# deposits_data = []
# savings_data = []

# params = {
#     'auth': API_KEY,
#     'topFinGrpNo': '020000',
#     'pageNo': 1,
# }

# # 정기예금 목록 저장
# response = requests.get(DP_URL, params=params).json()
# baseList = response.get('result').get('baseList')  # 상품 목록
# for product in baseList:
#     financial_products.append(product['fin_prdt_cd'])
#     deposits_data.append(product)

# # 적금 목록 저장
# response = requests.get(SP_URL, params=params).json()
# baseList = response.get('result').get('baseList')  # 상품 목록
# for product in baseList:
#     financial_products.append(product['fin_prdt_cd'])
#     savings_data.append(product)

# # 더미 데이터 생성 및 JSON 파일 저장
# file = OrderedDict()
# username_list = []
# N = 1000  # 예제에서는 1000명의 유저 데이터 생성
# i = 0

# while i < N:
#     rn = random_name()
#     if rn in username_list:
#         continue

#     username_list.append(rn)
#     i += 1

# # 현재 파일이 있는 디렉토리
# current_dir = os.path.dirname(os.path.abspath(__file__))
# save_dir = os.path.join(current_dir, 'user_data.json')

# with open(save_dir, 'w', encoding="utf-8") as f:
#     f.write('[')

#     for i in range(N):
#         # 랜덤한 데이터를 삽입
#         file['model'] = 'user.User'
#         file['pk'] = i + 1
#         file['fields'] = {
#             'username': username_list[i],
#             'nickname': random_name(),
#             'name': random_name(),
#             'email': f"{username_list[i]}@example.com",
#             'profile_img': 'images/user.png',
#             'financial_products': ','.join(
#                 [random.choice(financial_products) for _ in range(random.randint(0, 5))]
#             ),
#             'age': random.randint(18, 80),
#             'now_money': random.randint(10000, 1000000),
#             'money_per_year': random.randint(30000, 200000),
#             'desire_amount_saving': random.randint(10000, 500000),
#             'desire_amount_deposit': random.randint(10000, 500000),
#             'deposit_period': random.randint(1, 60),
#             'saving_period': random.randint(1, 60),
#             'fav_place': random.choice(['서울', '부산', '대구', '인천', '광주', '대전', '울산']),
#             'is_superuser': False,
#             'deposits': random.sample([d['fin_prdt_cd'] for d in deposits_data], k=random.randint(0, 5)),
#             'savings': random.sample([s['fin_prdt_cd'] for s in savings_data], k=random.randint(0, 5))
#         }

#         json.dump(file, f, ensure_ascii=False, indent='\t')
#         if i != N - 1:
#             f.write(',')
#     f.write(']')
#     f.close()

# print(f'데이터 생성 완료 / 저장 위치: {save_dir}')


### 로드 데이터는 MtM 필드에 적용되지 않는다. 그러니깐 다른 방법으로

# import os
# import django
# import random
# import requests
# from django.core.files.base import ContentFile
# from io import BytesIO
# import sys

# # Django 환경 설정 로드
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pjt.settings') 
# django.setup()

# from django.contrib.auth import get_user_model
# from compare.models import Deposit, Saving

# User = get_user_model()

# # 샘플 데이터
# first_name_samples = '김이박최정강조윤장임'
# middle_name_samples = '민서예지도하주윤채현지'
# last_name_samples = '준윤우원호후서연아은진'

# # 랜덤 이름 생성 함수
# def random_name():
#     result = ''
#     result += random.choice(first_name_samples)
#     result += random.choice(middle_name_samples)
#     result += random.choice(last_name_samples)
#     return result + str(random.randint(1, 100))

# # 현재 API에 들어있는 금융 상품 코드 리스트 저장
# DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
# SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
# API_KEY = '074e4e4a11eff3c68e5cd75a1e2b442a'

# financial_products = []
# deposits_data = []
# savings_data = []

# params = {
#     'auth': API_KEY,
#     'topFinGrpNo': '020000',
#     'pageNo': 1,
# }

# # 정기예금 목록 저장
# response = requests.get(DP_URL, params=params).json()
# baseList = response.get('result').get('baseList')  # 상품 목록
# for product in baseList:
#     financial_products.append(product['fin_prdt_cd'])
#     deposits_data.append(product)

# # 적금 목록 저장
# response = requests.get(SP_URL, params=params).json()
# baseList = response.get('result').get('baseList')  # 상품 목록
# for product in baseList:
#     financial_products.append(product['fin_prdt_cd'])
#     savings_data.append(product)

# # 더미 데이터 생성 및 DB에 저장
# username_list = []
# N = 1000  # 예제에서는 1000명의 유저 데이터 생성
# i = 0

# while i < N:
#     rn = random_name()
#     if rn in username_list:
#         continue

#     username_list.append(rn)
#     i += 1

#     user = User.objects.create(
#         username=rn,
#         nickname=random_name(),
#         name=random_name(),
#         email=f"{rn}@example.com",
#         profile_img='images/user.png',
#         financial_products=','.join(
#             [random.choice(financial_products) for _ in range(random.randint(0, 5))]
#         ),
#         age=random.randint(18, 80),
#         now_money=random.randint(10000, 1000000),
#         money_per_year=random.randint(30000, 200000),
#         desire_amount_saving=random.randint(10000, 500000),
#         desire_amount_deposit=random.randint(10000, 500000),
#         deposit_period=random.randint(1, 60),
#         saving_period=random.randint(1, 60),
#         fav_place=random.choice(['서울', '부산', '대구', '인천', '광주', '대전', '울산']),
#         is_superuser=False,
#     )

#     # ManyToMany 관계 설정
#     deposit_objects = Deposit.objects.filter(fin_prdt_cd__in=random.sample([d['fin_prdt_cd'] for d in deposits_data], k=random.randint(0, 5)))
#     saving_objects = Saving.objects.filter(fin_prdt_cd__in=random.sample([s['fin_prdt_cd'] for s in savings_data], k=random.randint(0, 5)))

#     user.deposits.set(deposit_objects)
#     user.savings.set(saving_objects)
#     user.save()

# print('데이터 생성 완료')


import os
import sys
import django
import random
import requests
from collections import OrderedDict

# Django 환경 설정 로드
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pjt.settings')  # 'django_pjt'를 실제 프로젝트 이름으로 대체
django.setup()

from django.contrib.auth import get_user_model
from compare.models import Deposit, Saving
from real_estate.models import RealEstate

User = get_user_model()

# 샘플 데이터
first_name_samples = '김이박최정강조윤장임'
middle_name_samples = '민서예지도하주윤채현지'
last_name_samples = '준윤우원호후서연아은진'

# 랜덤 이름 생성 함수
def random_name():
    result = ''
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result + str(random.randint(1, 100))

# 현재 API에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
API_KEY = '074e4e4a11eff3c68e5cd75a1e2b442a'

financial_products = []
deposits_data = []
savings_data = []

params = {
    'auth': API_KEY,
    'topFinGrpNo': '020000',
    'pageNo': 1,
}

# 정기예금 목록 저장
response = requests.get(DP_URL, params=params).json()
baseList = response.get('result').get('baseList')  # 상품 목록
for product in baseList:
    financial_products.append(product['fin_prdt_cd'])
    deposits_data.append(product)

# 적금 목록 저장
response = requests.get(SP_URL, params=params).json()
baseList = response.get('result').get('baseList')  # 상품 목록
for product in baseList:
    financial_products.append(product['fin_prdt_cd'])
    savings_data.append(product)

# 고유한 지역 리스트 가져오기
fav_places = list(RealEstate.objects.values_list('region', flat=True).distinct())

# 더미 데이터 생성 및 DB에 저장
username_list = []
N = 1000  # 예제에서는 1000명의 유저 데이터 생성
i = 0

real_estates = []

# 부동산 데이터 생성
for place in fav_places:
    for _ in range(50):  # 각 지역에 대해 50개의 부동산 데이터를 생성
        real_estate = RealEstate.objects.create(
            region=place,
            date_time='2024-01-01',  # 예시 날짜, 실제로는 적절한 날짜로 변경 필요
            price=random.randint(100000000, 1000000000)
        )
        real_estates.append(real_estate)

while i < N:
    rn = random_name()
    if rn in username_list:
        continue

    username_list.append(rn)
    i += 1

    fav_place = random.choice(fav_places)

    user = User.objects.create(
        username=rn,
        nickname=random_name(),
        name=random_name(),
        email=f"{rn}@example.com",
        profile_img='images/user.png',
        financial_products=','.join(
            [random.choice(financial_products) for _ in range(random.randint(0, 5))]
        ),
        age=random.randint(18, 80),
        now_money=random.randint(10000, 1000000),
        money_per_year=random.randint(30000, 200000),
        desire_amount_saving=random.randint(10000, 500000),
        desire_amount_deposit=random.randint(10000, 500000),
        deposit_period=random.randint(1, 60),
        saving_period=random.randint(1, 60),
        fav_place=fav_place,
        is_superuser=False,
    )

    # ManyToMany 관계 설정
    deposit_objects = Deposit.objects.filter(fin_prdt_cd__in=random.sample([d['fin_prdt_cd'] for d in deposits_data], k=random.randint(0, 5)))
    saving_objects = Saving.objects.filter(fin_prdt_cd__in=random.sample([s['fin_prdt_cd'] for s in savings_data], k=random.randint(0, 5)))
    user.deposits.set(deposit_objects)
    user.savings.set(saving_objects)

    # 사용자의 선호 지역과 일치하는 부동산 데이터 추가
    user_real_estates = RealEstate.objects.filter(region=fav_place)
    user.real_estates.set(random.sample(list(user_real_estates), k=random.randint(1, 5)))

    user.save()

print('데이터 생성 완료')
