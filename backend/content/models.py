from django.db import models
from taggit.managers import TaggableManager

from backend.settings import (
    LEN_PHONE,
    MAX_LEN_CHAR,
    MAX_LEN_NAME_FEEDBACK,
    MAX_LEN_TEXT_FEEDBACK,
    MAX_LENGTH_EMAIL,
)
from users.models import User

from .validators import (
    EmailValidator,
    NameFeedbackUserkValidator,
    PhoneValidator,
    TextFeedbackValidator,
)


class PlatformAbout(models.Model):
    '''Информация о проекте Платформа.'''

    # photo = models.ImageField(upload_to='content/%Y/%m/%d/', blank=True)
    # # еще не определились надо ли менять фото из админки
    about_us = models.TextField(verbose_name='Описание раздела "О нас"')
    platform_email = models.EmailField(
        verbose_name='email Платформы',
        max_length=MAX_LENGTH_EMAIL,
        validators=[EmailValidator.validate_email],
    )

    class Meta:
        verbose_name = 'О платформе'
        verbose_name_plural = 'О платформе'


class Valuation(models.Model):
    '''Ценности проекта Платформа.'''

    title = models.CharField(verbose_name='Заголовок', max_length=MAX_LEN_CHAR)
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
        max_length=MAX_LEN_NAME_FEEDBACK,
        validators=[NameFeedbackUserkValidator.validate_name],
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=LEN_PHONE,
        validators=[PhoneValidator.validate_phone],
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL, validators=[EmailValidator.validate_email]
    )
    text = models.CharField(
        verbose_name='Текст обращения',
        max_length=MAX_LEN_TEXT_FEEDBACK,
        validators=[TextFeedbackValidator.validate_text],
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время обращения', auto_now_add=True
    )
    processed_at = models.DateTimeField(
        verbose_name='Дата и время обработки',
        # auto_now=True,
        null=True,
        blank=True,
    )
    status = models.BooleanField(verbose_name='Обработано', default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class News(models.Model):
    '''Новости Платформы.'''

    picture = models.ImageField(upload_to='news/%Y/%m/%d/', blank=True)
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=MAX_LEN_CHAR,
    )
    text = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    tags = TaggableManager()
    author = models.ForeignKey(
        User,
        verbose_name='Автор новостей',
        on_delete=models.CASCADE,
        related_name='news',
    )

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


class City(models.Model):
    '''Справочник городов.'''

    name = models.CharField(verbose_name='Город', max_length=MAX_LEN_CHAR)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Skills(models.Model):
    '''Навыки волонтеров.'''

    name = models.CharField(verbose_name='Навык', max_length=MAX_LEN_CHAR)
    description = models.TextField(verbose_name='Описание навыка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


# Активности под вопросом, высока вероятность что не будет в проекте
class Activities(models.Model):
    '''Необходимые активности для реализации проекта.'''

    name = models.CharField(verbose_name='Активность', max_length=MAX_LEN_CHAR)
    description = models.TextField(verbose_name='Описание активности')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'
