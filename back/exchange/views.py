from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
# Create your views here.
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from .models import Exchange
from .serializers import ExchangeSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
import requests
api_key = "IAfSKrdJnoyMS13XKyyBN75yJ6NgmXHs"
date = '20240517'
URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate={date}&data=AP01'


@api_view(['GET'])
def get_exchange_data(request):
    response = requests.get(URL).json()
    exist_response = Exchange.objects.all() # 전체 항목
    if response:
        if not exist_response: # 현재 존재하는 데이터가 없다면
                serializer = ExchangeSerializer(data=response, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else:
            Exchange.objects.all().delete() # 현재 존재하는 데이터가 있다면 밀어버린다. -> 최신화 
            serializer = ExchangeSerializer(data=response, many=True)     
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    serializer = ExchangeSerializer(exist_response, many=True)
    return Response(serializer.data)
