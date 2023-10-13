from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator
from taggit.managers import TaggableManager

from backend.settings import (MAX_LEN_CHAR,
                              MAX_LEN_PHONE,
                              MESSAGE_PHONE_REGEX)


class PlatformAbout(models.Model):
    '''Информация о проекте Платформа.'''

    # photo = models.ImageField(upload_to='content/%Y/%m/%d/', blank=True)
    # # еще не определились надо ли менять фото из админки
    about_us = models.TextField(verbose_name='Описание раздела "О нас"')
    platform_email = models.EmailField(
        verbose_name='email Платформы',
        max_length=MAX_LEN_CHAR,
    )

    class Meta:
        verbose_name = 'О платформе'
        verbose_name_plural = 'О платформе'


class Valuation(models.Model):
    '''Ценности проекта Платформа.'''

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=MAX_LEN_CHAR
    )
    description = models.TextField(verbose_name='Описание ценности')

    class Meta:
        verbose_name = 'Ценность платформы'
        verbose_name_plural = 'Ценности платформы'

    def __str__(self):
        return self.title


class Feedback(models.Model):
    '''Модель обратной связи на Платформе.'''

    name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LEN_CHAR
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^(?:\+7|8)[0-9]{10}$',
                message=MESSAGE_PHONE_REGEX.format(MAX_LEN_PHONE),
            ),
            MaxLengthValidator(MAX_LEN_PHONE)
        ]
    )
    email = models.EmailField(max_length=MAX_LEN_CHAR)
    text = models.TextField(verbose_name='Текст обращения')
    created_at = models.DateTimeField(
        verbose_name='Дата и время обращения',
        auto_now_add=True
    )
    processed_at = models.DateTimeField(
        verbose_name='Дата и время обработки',
        auto_now=True
    )
    status = models.BooleanField(
        verbose_name='Обработано',
        default=False
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class News(models.Model):
    '''Новости Платформы.'''

    picture = models.ImageField(
        upload_to='news/%Y/%m/%d/',
        blank=True
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=MAX_LEN_CHAR,
    )
    text = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    tags = TaggableManager()
    author = models.CharField(max_length=15)
    # author = models.ForeignKey(
    #     User,
    #     verbose_name='Автор новостей',
    #     on_delete=models.CASCADE,
    #     related_name='news'
    # )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

#  Дополнительная возможно фича ачивка для волонтера  #  пока в разработке
# class Achievements(models.Model):
#     title = models.CharField(max_length=250)
#     description = models.TextField()
