from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from api.constants import PHONE_MAX_LEN, INVITE_CODE_MAX_LEN
from api.utils import generate_invite_code


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Номер телефона обязателен')
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    password = None
    phone = models.CharField(max_length=PHONE_MAX_LEN, unique=True)
    invite_code = models.CharField(
        max_length=INVITE_CODE_MAX_LEN,
        unique=True,
        default=generate_invite_code
    )
    used_invite_code = models.CharField(
        max_length=INVITE_CODE_MAX_LEN,
        blank=True,
        null=True,
        default=None
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('phone',)

    def __str__(self):
        return self.phone
