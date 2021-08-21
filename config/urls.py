"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


### 이메일 인증 ###
from dj_rest_auth.registration.views import VerifyEmailView
from users.views import ConfirmEmailView, ResendEmailView
### 이메일 인증 ###
### 비밀번호 재설정
from dj_rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/register/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    path('', include('diary.urls')),
    path('', include('users.urls')),

    ### 이메일 인증 좀 더 간단한 표현 ###
    path('send-confirmation-email/', ResendEmailView.as_view(), name='send-email-confirmation'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    ### 이메일 인증 좀 더 간단한 표현 ###

    ### 비밀번호 재설정 ###
    path('account/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    ### 비밀번호 재설정 ###

    ### 이메일 인증 ###
    # 이메일 관련 필요
    # path('accounts/allauth/', include('allauth.urls')),
    # path('send-confirmation-email/', ResendEmailView.as_view(), name='send-email-confirmation'),
    # 유효한 이메일이 유저에게 전달
    # re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    ### 이메일 인증 ###

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

