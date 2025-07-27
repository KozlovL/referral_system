from django.urls import path

from api.views import (
    Profile, UseInviteCode,
    SendCodeView, VerifyCodeView,
)

urlpatterns = [
    path('send_code/', SendCodeView.as_view()),
    path('verify_code/', VerifyCodeView.as_view()),
    path('profile/', Profile.as_view()),
    path('use_invite_code/', UseInviteCode.as_view()),
]
