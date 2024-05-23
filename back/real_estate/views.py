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
from .serializers import RealEstateSerializer
from .models import RealEstate
from datetime import datetime
from django.core.exceptions import ValidationError

REAL_ESTATE_API_KEY = 'a8T35jcnXvB0LAPhYhzpijuU%2BYcuu8AYpck3L1FSmoHiBxNQWw%2FQBQ9qGB7eKKeBxP3VojixO%2F0navzqDV1SIg%3D%3D'
URL = f'https://api.odcloud.kr/api/15069826/v1/uddi:c921d88a-6deb-4904-a658-e1fdb5437c92?page=1&perPage=236&serviceKey={REAL_ESTATE_API_KEY}'


from collections import Counter
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import User

import requests
from .serializers import RealEstateSerializer
from .models import RealEstate
from datetime import datetime
from django.core.exceptions import ValidationError

REAL_ESTATE_API_KEY = 'a8T35jcnXvB0LAPhYhzpijuU%2BYcuu8AYpck3L1FSmoHiBxNQWw%2FQBQ9qGB7eKKeBxP3VojixO%2F0navzqDV1SIg%3D%3D'
URL = f'https://api.odcloud.kr/api/15069826/v1/uddi:c921d88a-6deb-4904-a658-e1fdb5437c92?page=1&perPage=236&serviceKey={REAL_ESTATE_API_KEY}'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def make_data(request):
    
    if RealEstate.objects.exists():
        return Response({'message': 'Data already exists.'}, status=status.HTTP_200_OK)

    real_estate_data = requests.get(URL).json()

    # 데이터 가공 및 저장
    try:
        for entry in real_estate_data.get('data', []):
            region = entry.get('지 역')  # 지역 설정

            if not region:
                continue  # 지역 정보가 없는 경우 건너뜀

            # 날짜와 가격 데이터 추출
            for key, value in entry.items():
                if key == '지 역':
                    continue
                date_time = key
                price = value

                # 디버깅 로그 추가
                print(f"Processing entry - date_time: {date_time}, price: {price}, region: {region}")

                # date_time과 price가 None이 아닌지 확인
                if date_time and price is not None:
                    # 날짜 형식 변환
                    try:
                        datetime.strptime(date_time, '%Y-%m')
                    except ValueError:
                        print(f"Skipping invalid date format: {date_time}")
                        continue  # 잘못된 날짜 형식은 무시

                    # 데이터 저장
                    real_estate, created = RealEstate.objects.update_or_create(
                        date_time=date_time,
                        region=region,  # date_time과 region을 키로 설정
                        defaults={
                            'price': price,
                            'region': region
                        }
                    )
                    # 디버깅 로그 추가
                    if created:
                        print(f"Created new RealEstate: {real_estate}")
                    else:
                        print(f"Updated existing RealEstate: {real_estate}")

        # 저장된 데이터의 총 개수를 반환하여 확인
        total_count = RealEstate.objects.count()
        print(f"Total RealEstate records: {total_count}")

        return Response({'message': 'Data successfully created or updated.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 디버깅 로그 추가
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_regions(request):
    regions = RealEstate.objects.values_list('region', flat=True).distinct()
    return Response(regions, status=status.HTTP_200_OK)

from rest_framework import generics, permissions

class RealEstateListCreateView(generics.ListCreateAPIView):
    queryset = RealEstate.objects.all()
    serializer_class = RealEstateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_recent_real_estate(request, region):
    recent_real_estate = RealEstate.objects.filter(region=region, price__isnull=False).order_by('-date_time').first()
    if recent_real_estate:
        return Response({
            'id': recent_real_estate.id,
            'price': recent_real_estate.price,
            'date_time': recent_real_estate.date_time
        })
    return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def link_real_estate_to_user(request):
    real_estate_id = request.data.get('real_estate_id')
    user = request.user
    real_estate = get_object_or_404(RealEstate, id=real_estate_id)
    real_estate.users.add(user)
    return Response({'detail': 'Real estate linked successfully.'})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def unlink_real_estate_from_user(request, real_estate_id):
    real_estate = get_object_or_404(RealEstate, id=real_estate_id)
    user = request.user
    real_estate.users.remove(user)
    return JsonResponse({'status': 'unlinked'})