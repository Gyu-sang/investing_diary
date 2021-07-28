from django.urls import path, include 
from .views import helloAPI, DiaryFeed

urlpatterns = [
    path('hello/', helloAPI),
    path('feed/', DiaryFeed),
]