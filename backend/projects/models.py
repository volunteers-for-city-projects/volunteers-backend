from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MaxLengthValidator,
    MinLengthValidator,
)
from django.core.validators import RegexValidator
from datetime import date

from content.models import City, Skills  # Activities
from users.models import User
from backend.settings import (
    MAX_LEN_NAME,
    LEN_OGRN,
    MAX_LEN_PHONE,
    MESSAGE_PHONE_REGEX,
    ORGANIZATION,
    VOLUNTEER,
    PROJECT,
    PROJECTPARTICIPANTS,
    MAX_LEN_TELEGRAM,
    MIN_LEN_TELEGRAM,
)


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
    ogrn = models.CharField(
        max_length=LEN_OGRN,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='ОГРН должен состоять только из цифр.',
            ),
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
        max_length=MAX_LEN_PHONE,
        blank=False,
        verbose_name='Телефон',
    )
    about = models.TextField(
        blank=False,
        verbose_name='Об организации',
    )
    city = models.OneToOneField(
        City,
        blank=False,
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
        max_length=MAX_LEN_TELEGRAM,
        validators=[
            RegexValidator(
                regex=r'^@[\w]+$',
                message=(
                    'Ник в Telegram должен начинаться с @ и содержать '
                    'только буквы, цифры и знаки подчеркивания.',
                ),
            ),
            MinLengthValidator(MIN_LEN_TELEGRAM),
            MaxLengthValidator(MAX_LEN_TELEGRAM),
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
    # activities = models.ForeignKey(
    #     Activities,
    #     on_delete=models.CASCADE,
    #     verbose_name='Активности',
    # )
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
    """
    Модель представляет собой категории проекта.
    """

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


class Project(models.Model):
    """
    Модель представляет собой информацию о проекте.
    """

    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'
    OPEN = 'open'
    READY_FOR_FEEDBACK = 'ready_for_feedback'
    RECEPTION_OF_RESPONSES_CLOSED = 'Reception_of_responses_closed'
    PROJECT_COMPLETED = 'project_completed'

    STATUS_PROJECT = [
        (OPEN, 'Открыт'),
        (READY_FOR_FEEDBACK, 'Готов к откликам'),
        (RECEPTION_OF_RESPONSES_CLOSED, 'Прием откликов окончен'),
        (PROJECT_COMPLETED, 'Проект завершен'),
    ]

    STATUS_CHOICES = [
        (APPROVED, 'Одобрено'),
        (PENDING, 'На рассмотрении'),
        (REJECTED, 'Отклонено'),
    ]

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
        null=True,
        blank=True,
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
    # activities = models.ManyToManyField(
    #     Activities,
    #     related_name='projects',
    #     verbose_name='Активности',
    # )
    organization = models.ForeignKey(
        Organization,
        blank=False,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Организация',
    )
    city = models.ForeignKey(
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
    status_project = models.CharField(
        max_length=100,
        choices=STATUS_PROJECT,
        null=True,
        blank=True,
        default=None,
        verbose_name='Статус проекта',
    )
    photo_previous_event = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Фото с мероприятия',
    )
    # tags =
    participants = models.ForeignKey(
        'ProjectParticipants',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='projects',
        verbose_name='Участники',
    )
    status_approve = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING,
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
