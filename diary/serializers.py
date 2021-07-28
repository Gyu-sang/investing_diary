from rest_framework import serializers
from .models import Corporation, Diary 

class CorporationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Corporation
        fields = ['name', 'logo']

class DiarySerializer(serializers.ModelSerializer):
    buy = CorporationSerializer(many=True)
    sell = CorporationSerializer(many=True)

    class Meta : 
        model = Diary 
        fields = ['user', 'content', 'buy', 'sell']