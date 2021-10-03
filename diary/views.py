from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, action
from .models import Diary, BuySell, Corporation, FavoriteCorporation, Like
from .serializers import DiarySerializer, BuySellSerializer, CorporationSerializer, FavoriteCorporationSerializer, LikeSerializer, LikeListSerializer
from .permissions import IsOwner
from rest_framework import viewsets 
from django.db.models import Q, Count

# Create your views here.

@api_view(['GET'])
def helloAPI(request):
    return Response('hello world')


# @api_view(['GET'])
# @permission_classes([IsAuthenticated, IsOwner])
# def DiaryFeed(request):
#     totalDiary = Diary.objects.all()
#     serializer = DiarySerializer(totalDiary, many = True)
#     return Response(serializer.data)


# class DiaryViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsOwner]
#     queryset = Diary.objects.all() 
#     serializer_class = DiarySerializer 

#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return DiaryListSerializer
#         else :
#             return DiarySerializer


class DiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer 

    def get_queryset(self):
        user = self.request.user.id
        diary = Diary.objects.annotate(like_count=Count('like')).filter(
            like_count__lt = 5,
            # user = user    
        ).order_by('-createdAt')
        return diary

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        like = self.get_object()
        serializer = LikeListSerializer(like, context={'request': request})
        return Response(serializer.data)

    # @action(detail=False)
    # def user(self, request):
    #     user = self.request.user.id
    #     diary_list = Diary.objects.filter(user=user)
    #     serializer = DiarySerializer(diary_list, context={'request': request})
    #     return Response(serializer.data)


class PopularDiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Diary.objects.all() 
    serializer_class = DiarySerializer 

    def get_queryset(self):
        user = self.request.user.id
        diary = Diary.objects.annotate(like_count=Count('like')).filter(
            Q(like_count__gte = 5)
        ).order_by('-createdAt')
        return diary


class BuySellViewSet(viewsets.ModelViewSet):
    queryset = BuySell.objects.all()
    serializer_class = BuySellSerializer


class CorporationViewSet(viewsets.ModelViewSet):
    queryset = Corporation.objects.all() 
    serializer_class = CorporationSerializer 

    # def get_queryset(self):
    #     user = self.request.user.id    
    #     corporation = Corporation.objects.all().filter(
    #         Q(favoritecorporation__user_id = user) | 
    #         Q(favoritecorporation__isnull=True)
    #     ).order_by('-favoritecorporation__updatedAt')
    #     return corporation


class FavoriteCorporationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = FavoriteCorporation.objects.all()
    serializer_class = FavoriteCorporationSerializer

    def get_queryset(self):
        user = self.request.user.id
        favoritecorporation = FavoriteCorporation.objects.filter(user=user).order_by('-updatedAt')
        return favoritecorporation


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer