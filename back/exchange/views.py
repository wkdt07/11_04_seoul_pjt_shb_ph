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
api_key = "a8T35jcnXvB0LAPhYhzpijuU%2BYcuu8AYpck3L1FSmoHiBxNQWw%2FQBQ9qGB7eKKeBxP3VojixO%2F0navzqDV1SIg%3D%3D"




URL = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'


@api_view(['GET'])
def get_exchange_data(request):
    response = requests.get(URL).json()
    exist_response = Exchange.objects.all() # 전체 항목
    if response:
        if not exist_response:
                serializer = ExchangeSerializer(data=response, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else:
            Exchange.objects.all().delete()
            serializer = ExchangeSerializer(data=response, many=True)     
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    serializer = ExchangeSerializer(exist_response, many=True)
    return Response(serializer.data)
