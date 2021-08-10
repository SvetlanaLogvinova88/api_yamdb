from django.contrib.auth.models import AbstractUser
from django.db import models

from . managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(
        "Адрес e-mail",
        unique=True,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.SlugField(
        "Роль пользователя",
    )
    error_messages={
            'unique': "Пользователь с указанным e-mail уже зарегистрирован.",
        }

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
