from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from .models import Diary 
from .serializers import DiarySerializer, DiaryListSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework import viewsets 


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


class DiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Diary.objects.all() 
    serializer_class = DiarySerializer 

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DiaryListSerializer
        else :
            return DiarySerializer