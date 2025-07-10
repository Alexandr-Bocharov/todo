from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model


class User(AbstractUser):
    username = None
    login = models.CharField(
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer."),
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.login

