from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# from users.validators import username_validator

USER_ROLES = [
    ('admin', 'Администратор'),
    ('organizer', 'Организатор'),
    ('volunteer', 'Волонтер'),
]


class User(AbstractUser):
    # username = models.CharField(
    #     verbose_name='Пользователь',
    #     max_length=settings.MAX_LENGTH_USERNAME,
    #     unique=True,
    #     validators=(UnicodeUsernameValidator(), username_validator,)
    # )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LENGTH_NAME,
        blank=False
    )
    second_name = models.CharField(
        verbose_name='Отчество',
        max_length=settings.MAX_LENGTH_NAME,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LENGTH_NAME,
        blank=False
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        blank=False
    )
    role = models.CharField(
        'Роль',
        choices=USER_ROLES,
        max_length=50,
        default='volunteer'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'second_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.second_name}'
