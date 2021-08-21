from rest_framework import serializers
from .models import Corporation, Diary, BuySell, Like, FavoriteCorporation
from users.models import Profile, User
from users.serializers import ProfileSerializer, OtherUserSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from django.utils import timezone

class FavoriteCorporationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta :
        model = FavoriteCorporation
        fields = ['id', 'updatedAt', 'corporation', 'user']    


class CorporationSerializer(serializers.ModelSerializer):
    isFavorite = serializers.SerializerMethodField()
    # lastUsedAt = serializers.SerializerMethodField()

    class Meta :
        model = Corporation
        fields = ['id','name', 'logo','code','isFavorite']
        read_only_fields = ['name', 'logo', 'code','isFavorite']

    def get_isFavorite(self, obj):
        requestUser = self.context['request'].user
        return FavoriteCorporation.objects.filter(corporation=obj, user=requestUser).exists()

    # def get_lastUsedAt(self, obj):
    #     requestUser = self.context['request'].user
    #     try :
    #         res = FavoriteCorporation.objects.get(corporation=obj, user=requestUser).updatedAt
    #     except :
    #         res = False
    #     return res


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = Like
        fields = ['user','diary','updatedAt']  

    def to_representation(self, obj):
        res = super().to_representation(obj)
        res.update({'user': OtherUserSerializer(obj.user, context=self.context).data})
        return res


class LikeListSerializer(serializers.ModelSerializer):
    like = LikeSerializer(read_only=True, source='like_set', many=True)
    like_count = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()

    class Meta : 
        model = Diary 
        fields = ['like_count','isLiked','like']
    
    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_isLiked(self, obj):
        requestUser = self.context['request'].user
        return Like.objects.filter(diary=obj, user=requestUser).exists()


class BuySellSerializer(serializers.ModelSerializer):
    class Meta :
        model = BuySell
        fields = ['id','corporation','category','price','quantity','reason']

    def to_representation(self, obj):
        res = super().to_representation(obj)
        res.update({'corporation': CorporationSerializer(obj.corporation, context=self.context).data})
        return res


class DiarySerializer(WritableNestedModelSerializer):  
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    buysell = BuySellSerializer(source='buysell_set', many=True)    
    like_count = serializers.SerializerMethodField()
    isMine = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    recommendationType = serializers.SerializerMethodField()

    class Meta : 
        model = Diary 
        fields = ['id','user','content', 'buysell','createdAt','updatedAt','like_count', 'isLiked', 'isMine', 'recommendationType']
        # read_only_fields = ['like_count', 'isMine','isLiked','recommendationType']

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_isMine(self, obj):
        requestUser = self.context['request'].user
        return obj.user == requestUser

    def get_isLiked(self, obj):
        requestUser = self.context['request'].user
        return Like.objects.filter(diary=obj, user=requestUser).exists()

    def get_recommendationType(self, obj):
        recommendationNum = Like.objects.filter(diary=obj).count()
        if recommendationNum >= 5:
            return True
        else :
            return False 

    def to_representation(self, obj):
        res = super().to_representation(obj)
        res.update({'user': OtherUserSerializer(obj.user, context=self.context).data})
        return res