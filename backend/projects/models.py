from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)

from django.core.validators import RegexValidator
from datetime import date

MAX_LEN_NAME = 200
LEN_OGRN = 13
MAX_LEN_PHONE = 11
MESSAGE_PHONE_REGEX = (
    'Номер телефона должен начинаться с +7 или 8 и содержать {} цифр.',
)


class Organization(models.Model):
    contact_person = models.OneToOneField(
        # User,
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
        # City,
        # on_delete=models.CASCADE,
        related_name='organization',
        verbose_name='Город',
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    user = models.OneToOneField(
        # User,
        related_name='volunteer',
        verbose_name='Пользователь',
    )
    city = models.OneToOneField(
        # City,
        # on_delete=models.CASCADE,
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
        # Skills,
        # on_delete=models.CASCADE,
        verbose_name='Навыки',
    )
    photo = models.ImageField(
        blank=False,
        verbose_name='Фото',
    )
    activities = models.ForeignKey(
        "app.Model",
        verbose_name='Активности',
        # on_delete=models.CASCADE,
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
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'

    def __str__(self):
        return self.user


class StatusApprove(models.Model):
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
        verbose_name = 'Статус проверки'
        verbose_name_plural = 'Статусы проверки'

    def __str__(self):
        return self.title


class Project(models.Model):
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
    application_date = models.DateTimeField()
    event_purpose = models.TextField(
        blank=False,
        verbose_name='Цель мероприятия',
    )
    # event_card
    # activities = models.ManyToManyField(
    #     Activity,
    #     related_name='projects',
    #     verbose_name='Активности',
    # )
    organization = models
    city = models.OneToOneField(
        # City,
        blank=False,
        # on_delete=models.CASCADE,
        related_name='project',
        verbose_name='Город',
    )
    category = models.ForeignKey(
        # Category,
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
        verbose_name='',
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
        return self.name


class ProjectParticipants(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'

    def __str__(self):
        return self.name
