from accounts.models import User
from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
import requests
from .serializer import *
from models import *




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
