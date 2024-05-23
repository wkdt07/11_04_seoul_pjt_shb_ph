from rest_framework import serializers
from .models import RealEstate

class RealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['date_time'] = instance.date_time[:7]  # 'YYYY-MM' 포맷 유지
        return ret