import time
from http import HTTPStatus

from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.constants import AUTH_CODE
from api.models import User
from api.serializers import (
    PhoneSerializer, AuthSerializer, UserSerializer,
    InviteCodeSerializer,
)


class SendCodeView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        # Сохраняем код в кэш
        cache.set(f"auth_code:{phone}", AUTH_CODE)
        time.sleep(2)
        return Response({'detail': 'Код отправлен.'}, status=HTTPStatus.OK)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        real_code = cache.get(f"auth_code:{phone}")
        if not real_code or real_code != code:
            return Response({
                'code': 'Неверный или просроченный код.',
            }, status=HTTPStatus.BAD_REQUEST)
        # Удалим код после успешной авторизации
        cache.delete(f"auth_code:{phone}")
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=HTTPStatus.OK)


class UseInviteCode(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        if user.used_invite_code:
            return Response(
                {'detail': 'Вы уже активировали инвайт-код.'},
                status=HTTPStatus.BAD_REQUEST
            )
        serializer = InviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['invite_code']
        if not User.objects.filter(invite_code=code).exists():
            return Response({
                'detail': 'Код не найден.'
            }, status=HTTPStatus.BAD_REQUEST)
        user.used_invite_code = code
        user.save()
        return Response({
            'detail': 'Код успешно активирован.'
        }, status=HTTPStatus.OK)
