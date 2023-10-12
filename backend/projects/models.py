from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

MAX_LEN_NAME = 200
LEN_OGRN = 13
MAX_LEN_PHONE = 11
MESSAGE_PHONE_REGEX = (
    'Номер телефона должен начинаться с +7 или 8 и содержать {} цифр.',
)


class Organization(models.Model):
    # contact_person =
    title = models.CharField(
        max_length=MAX_LEN_NAME,
        blank=False,
        verbose_name='Название',
    )
    ogrn = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(LEN_OGRN),
            MinValueValidator(LEN_OGRN),
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
            MaxValueValidator(MAX_LEN_PHONE),
        ],
        max_length=11,
        blank=True,
        verbose_name='Телефон',
    )
    about = models.TextField(
        blank=False,
        verbose_name='Об организации',
    )
    # city = models.OneToOneField(
    #     City,
    #     on_delete=models.CASCADE,
    #     related_name='project',
    #     verbose_name='Город',
    # )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    class Meta:
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'

    def __str__(self):
        return self.name


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
    # city = models.OneToOneField(
    #     City,
    #     on_delete=models.CASCADE,
    #     related_name='project',
    #     verbose_name='Город',
    # )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name
