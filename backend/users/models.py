from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import EmailValidator

from .validators import NameUserValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ADMIN = 'admin'
    ORGANIZER = 'organizer'
    VOLUNTEER = 'volunteer'

    USER_ROLES = [
        (ADMIN, 'Администратор'),
        (ORGANIZER, 'Организатор'),
        (VOLUNTEER, 'Волонтер'),
    ]

    username = None
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.MAX_LEN_NAME_USER,
        blank=False,
        validators=[NameUserValidator.validate_name],
    )
    second_name = models.CharField(
        verbose_name='Отчество',
        max_length=settings.MAX_LEN_NAME_USER,
        blank=False,
        validators=[NameUserValidator.validate_name],
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.MAX_LEN_NAME_USER,
        blank=False,
        validators=[NameUserValidator.validate_name],
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
        blank=False,
        validators=[EmailValidator.validate_email],
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=USER_ROLES,
        max_length=settings.MAX_LENGTH_ROLE,
        blank=False,
        default=ADMIN
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'second_name', 'last_name', 'role',)

    @property
    def is_organizer(self):
        return self.role == self.ORGANIZER

    @property
    def is_volunteer(self):
        return self.role == self.VOLUNTEER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('date_joined',)

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.second_name} '
                f'{self.email}')
