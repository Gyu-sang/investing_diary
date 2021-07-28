from rest_framework.response import Response 
from rest_framework.decorators import api_view 
from .models import Diary 
from .serializers import DiarySerializer

# Create your views here.

@api_view(['GET'])
def helloAPI(request):
    return Response('hello world')


@api_view(['GET'])
def DiaryFeed(request):
    totalDiary = Diary.objects.all()
    serializer = DiarySerializer(totalDiary, many = True)
    return Response(serializer.data)


