from django.urls import path, include 
from .views import helloAPI, DiaryViewSet, CorporationViewSet, PopularDiaryViewSet, LikeViewSet, FavoriteCorporationViewSet, BuySellViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('diary', DiaryViewSet)
router.register('corporation', CorporationViewSet)
router.register('populardiary', PopularDiaryViewSet)
router.register('like', LikeViewSet)
router.register('favoritecorporation', FavoriteCorporationViewSet)
router.register('buysell', BuySellViewSet)


urlpatterns = [
    path('hello/', helloAPI),
    # path('feed/', DiaryFeed),
    path('', include(router.urls))
]