from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = [
    ('admin', 'Администратор'),
    ('organizer', 'Организатор'),
    ('volunteer', 'Волонтер'),
]


class User(AbstractUser):
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
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
        blank=False
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=USER_ROLES,
        max_length=50,
        default='volunteer'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'second_name', 'last_name',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('date_joined',)

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.second_name} '
                f'{self.email}')
