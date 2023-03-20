from django.contrib.auth.models import AbstractUser
from django.db import models

from infra.base import Choice
from django.conf import settings


class UserType(Choice):
    BROKER = 'BROKER'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sayata_userprofile",
    )
    user_type =  models.TextField(UserType, default=UserType.BROKER)

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.get_or_create(user=user)[0]

    def __str__(self):
        return self.user.get_username()
