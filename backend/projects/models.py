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
