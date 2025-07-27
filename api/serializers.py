from rest_framework import serializers

from api.constants import PHONE_MAX_LEN
from api.models import User


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=PHONE_MAX_LEN)

    def validate_phone(self, phone):
        if not phone.isdigit():
            raise serializers.ValidationError(
                f'Номер должен содержать только цифры. {phone}'
                )
        return phone


class AuthSerializer(PhoneSerializer):
    code = serializers.CharField()


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

    def validate_invite_code(self, invite_code):
        if not User.objects.filter(invite_code=invite_code).exists():
            raise serializers.ValidationError('Реферальный код не существует.')
        return invite_code


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'phone',
            'invite_code',
            'invited_users',
            'used_invite_code',
        )

    def get_invited_users(self, user):
        return User.objects.filter(
            used_invite_code=user.invite_code
        ).values_list('phone', flat=True)
