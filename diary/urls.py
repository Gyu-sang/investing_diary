from django.urls import path, include 
from .views import helloAPI, DiaryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('diary', DiaryViewSet)

urlpatterns = [
    path('hello/', helloAPI),
    # path('feed/', DiaryFeed),
    path('', include(router.urls))
]