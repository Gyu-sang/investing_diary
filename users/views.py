from django.shortcuts import render
from rest_framework.response import Response 
from .models import Profile
from .serializers import ProfileSerializer
from diary.permissions import IsOwner
from diary.serializers import DiarySerializer
from diary.models import Diary
from rest_framework import viewsets 
from django.utils import timezone
from rest_framework.decorators import permission_classes, action

###### 이메일 ######
from django.core.mail.message import EmailMessage
from config import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
###### 이메일 ######


###### 이메일 인증 ######
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.http import HttpResponseRedirect, HttpResponse
from allauth.account.utils import send_email_confirmation
from allauth.account.admin import EmailAddress
from rest_framework import status
###### 이메일 인증 ######




# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(feedEndAt = timezone.now())

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


###### 이메일 ######
FROM_EMAIL = settings.EMAIL_HOST_USER
@api_view(['GET'])
@permission_classes([AllowAny])
def send_test_email(requset):
    subject = "이메일 테스트2"
    to = ['blueqnpfr@gmail.com']
    message = "email test가 성공했습니다."
    EmailMessage(subject=subject, body=message, to=to, from_email=FROM_EMAIL).send()

    return Response({"message": "ok"})
###### 이메일 ######


class ResendEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # user = get_object_or_404(User, email=request.data['email'])
        emailAddress = EmailAddress.objects.filter(user=request.user, verified=True).exists()

        if emailAddress:
            return Response({'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)


###### 이메일 인증 ######
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]




    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponse('이메일 인증 성공. 이제 서비스를 이용할 수 있습니다.')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return Response({"message": "failure"})  
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
###### 이메일 인증 ######
