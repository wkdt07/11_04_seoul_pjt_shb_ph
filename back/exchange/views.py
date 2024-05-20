# from django.shortcuts import render
# from rest_framework.decorators import api_view,permission_classes
# from rest_framework import status
# # Create your views here.
# from django.shortcuts import get_object_or_404, get_list_or_404
# from rest_framework.response import Response
# from .models import Exchange
# from .serializers import ExchangeSerializer
# from rest_framework.permissions import IsAuthenticated,IsAdminUser
# import requests
# api_key = "IAfSKrdJnoyMS13XKyyBN75yJ6NgmXHs"
# date = '20240517'
# URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={date}&data=AP01'


# @api_view(['GET'])
# def get_exchange_data(request):
#     response = requests.get(URL).json()
#     exist_response = Exchange.objects.all() # 전체 항목
#     if response:
#         if not exist_response: # 현재 존재하는 데이터가 없다면
#                 serializer = ExchangeSerializer(data=response, many=True)
#                 if serializer.is_valid(raise_exception=True):
#                     serializer.save()
#                     return Response(serializer.data)
#         else:
#             Exchange.objects.all().delete() # 현재 존재하는 데이터가 있다면 밀어버린다. -> 최신화 
#             serializer = ExchangeSerializer(data=response, many=True)     
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response(serializer.data)
#     serializer = ExchangeSerializer(exist_response, many=True)
#     return Response(serializer.data)
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Exchange
from .serializers import ExchangeSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import requests
import os
from rest_framework import generics

class ExchangeList(generics.ListAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

# 환경 변수에서 API 키를 가져옵니다.
API_KEY = os.getenv('EXCHANGE_API_KEY', 'IAfSKrdJnoyMS13XKyyBN75yJ6NgmXHs')
DATE = '20240517'
URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}&searchdate={DATE}&data=AP01'

def save_exchange_data(response):
    for item in response:
        # 'result'가 1인 경우에만 데이터를 저장합니다.
        if item.get('result') == 1:
            serializer = ExchangeSerializer(data=item)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_exchange_data(request):
    try:
        response = requests.get(URL)
        response.raise_for_status()
        exchange_data = response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if exchange_data:
        # 기존 데이터를 모두 삭제합니다.
        Exchange.objects.all().delete()
        save_exchange_data(exchange_data)
        return Response(exchange_data, status=status.HTTP_201_CREATED)

    # 기존 데이터가 없거나 API 호출에 실패한 경우 기존 데이터를 반환합니다.
    existing_data = Exchange.objects.all()
    serializer = ExchangeSerializer(existing_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
