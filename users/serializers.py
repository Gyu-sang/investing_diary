from rest_framework import serializers
from .models import User, Profile
from allauth.account.admin import EmailAddress
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = Profile
        fields = ['id','user','name', 'image', 'job', 'bio','investingStartedAt', 'feedEndAt', 'createdAt', 'updatedAt']
        read_only_fields = ['feedEndAt']


class UserSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    verified = serializers.SerializerMethodField()
    class Meta :
        model = User
        fields = ['id','email','profile','verified']
        read_only_fields = ['email','verified']

    def get_verified(self, obj):
        requestUser = self.context['request'].user
        try:
            return EmailAddress.objects.get(user=obj).verified
        except EmailAddress.DoesNotExist:
            return None


class OtherProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = ['name', 'image', 'job', 'bio','investingStartedAt']


class OtherUserSerializer(serializers.ModelSerializer):
    profile = OtherProfileSerializer(read_only=True)
    class Meta :
        model = User
        fields = ['id','profile']
        read_only_fields = ['email']