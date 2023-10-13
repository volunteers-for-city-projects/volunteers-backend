from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.core.validators import RegexValidator
from datetime import date

from content.models import City, Skills, Activities
from users.models import User

MAX_LEN_NAME = 200
LEN_OGRN = 13
MAX_LEN_PHONE = 11
MESSAGE_PHONE_REGEX = 'Номер должен начинаться с +7 или 8 и содержать {} цифр.'


ORGANIZATION = 'Название: {}> ОГРН: {}> Город: {}'
VOLUNTEER = 'Пользователь: {}> Город: {}> Навыки: {}'
PROJECT = 'Название: {}> Организатор: {}> Категория: {}> Город: {}'
PROJECTPARTICIPANTS = 'Проект: {}> Волонтер: {}'


class Organization(models.Model):
    """
    Модель представляет собой информацию об организации-организаторе проектов.
    """

    contact_person = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organization',
        verbose_name='Пользователь',
    )
    title = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=False,
        verbose_name='Название',
    )
    ogrn = models.PositiveIntegerField(
        validators=[
            MaxLengthValidator(LEN_OGRN),
            MinLengthValidator(LEN_OGRN),
        ],
        unique=True,
        blank=False,
        verbose_name='ОГРН',
    )
    phone = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|8)[0-9]{10}$',
                message=MESSAGE_PHONE_REGEX.format(MAX_LEN_PHONE),
            ),
            MaxLengthValidator(MAX_LEN_PHONE),
        ],
        max_length=11,
        blank=True,
        verbose_name='Телефон',
    )
    about = models.TextField(
        blank=False,
        verbose_name='Об организации',
    )
    city = models.OneToOneField(
        City,
        on_delete=models.CASCADE,
        related_name='organization',
        verbose_name='Город',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return ORGANIZATION.format(self.title, self.ogrn, self.city)


class Volunteer(models.Model):
    """
    Модель представляет собой информацию о волонтере.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer',
        verbose_name='Пользователь',
    )
    city = models.OneToOneField(
        City,
        on_delete=models.CASCADE,
        related_name='volunteer',
        verbose_name='Город',
    )
    telegram = models.CharField(
        max_length=32,
        validators=[
            RegexValidator(
                regex=r'^@[\w]+$',
                message=(
                    'Ник в Telegram должен начинаться с @ и содержать '
                    'только буквы, цифры и знаки подчеркивания.',
                ),
            ),
            MinLengthValidator(5),
            MaxLengthValidator(32),
        ],
    )
    skills = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='Навыки',
    )
    photo = models.ImageField(
        blank=False,
        verbose_name='Фото',
    )
    activities = models.ForeignKey(
        Activities,
        on_delete=models.CASCADE,
        verbose_name='Активности',
    )
    date_of_birth = models.DateField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today()),
        ],
        verbose_name='Дата рождения',
        help_text='Введите дату в формате "ДД.ММ.ГГГГ", пример: "01 01 2000".',
    )
    phone = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|8)[0-9]{10}$',
                message=MESSAGE_PHONE_REGEX.format(MAX_LEN_PHONE),
            ),
            MaxLengthValidator(MAX_LEN_PHONE),
        ],
        max_length=11,
        blank=True,
        verbose_name='Телефон',
    )

    class Meta:
        ordering = ['user__last_name']
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'

    def __str__(self):
        return VOLUNTEER.format(self.user, self.city, self.skills)


class Category(models.Model):
    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    slug = models.SlugField(
        unique=True, max_length=30, verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class StatusApprove(models.Model):
    """
    Модель представляет собой статус проверки проекта.
    """

    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (APPROVED, 'Одобрено'),
        (PENDING, 'На рассмотрении'),
        (REJECTED, 'Отклонено'),
    ]

    title = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name='Статус проверки',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Статус проверки'
        verbose_name_plural = 'Статусы проверки'

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    Модель представляет собой информацию о проекте.
    """

    name = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=False,
        verbose_name='Название',
    )
    description = models.TextField(
        blank=False,
        verbose_name='Описание',
    )
    picture = models.ImageField(
        blank=False,
        verbose_name='Картинка',
    )
    start_datatime = models.DateTimeField(
        blank=False,
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата начало мероприятия',
    )
    end_datatime = models.DateTimeField(
        blank=False,
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата окончания мероприятия',
    )
    application_date = models.DateTimeField(verbose_name='Дата подачи заявки')
    event_purpose = models.TextField(
        blank=False,
        verbose_name='Цель мероприятия',
    )
    # event_card
    activities = models.ManyToManyField(
        Activities,
        related_name='projects',
        verbose_name='Активности',
    )
    organization = models.ForeignKey(
        Organization,
        blank=False,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Организация',
    )
    city = models.OneToOneField(
        City,
        blank=False,
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='Город',
    )
    category = models.ForeignKey(
        Category,
        blank=False,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Категория',
    )
    photo_previous_event = models.ImageField(
        blank=False,
        verbose_name='Фото с мероприятия',
    )
    # tags =
    participants = models.ForeignKey(
        'ProjectParticipants',
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
        verbose_name='Участники',
    )
    status_approve = models.ForeignKey(
        StatusApprove,
        on_delete=models.CASCADE,
        verbose_name='Статус проверки',
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return PROJECT.format(
            self.name, self.organization, self.category, self.city
        )


class ProjectParticipants(models.Model):
    """
    Модель представляет собой список участников(волонтеров) проекта.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'

    def __str__(self):
        return PROJECTPARTICIPANTS.format(self.project, self.volunteer)
