from rest_framework import serializers
from .models import Corporation, Diary 
from users.models import Profile
from users.serializers import ProfileSerializer, UserSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer

class CorporationSerializer(serializers.ModelSerializer):

    class Meta :
        model = Corporation
        fields = ['name', 'logo']

class DiaryListSerializer(serializers.ModelSerializer):
    buy = CorporationSerializer(many=True)
    sell = CorporationSerializer(many=True)
    user = serializers.ReadOnlyField(source='email')
    
    class Meta : 
        model = Diary 
        fields = ['user','content', 'buy', 'sell']

class DiarySerializer(WritableNestedModelSerializer):
    # buy = serializers.SlugRelatedField(queryset=Corporation.objects.all(), many=True, slug_field='name')
    # sell = serializers.HyperlinkedRelatedField(queryset=Corporation.objects.all(), many=True, view_name='diary')
    
    buy = serializers.PrimaryKeyRelatedField(queryset=Corporation.objects.all(), many=True)
    sell = serializers.PrimaryKeyRelatedField(queryset=Corporation.objects.all(), many=True)

    # buy = serializers.StringRelatedField(many=True)
    # sell = serializers.StringRelatedField(many=True)
    user = serializers.ReadOnlyField(source='email')

    class Meta : 
        model = Diary 
        depth = 1
        fields = ['user','content', 'buy', 'sell']
