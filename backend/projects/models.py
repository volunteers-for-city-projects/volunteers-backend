from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from content.models import City, Skills
from users.models import User

from .validators import (
    LengthValidator,
    regex_string_validator,
    validate_about,
    validate_name,
    validate_ogrn,
    validate_phone_number,
    validate_telegram,
    validate_title,
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
        max_length=settings.MAX_LEN_TITLE,
        validators=[validate_title],
        blank=False,
        verbose_name='Название',
    )
    ogrn = models.CharField(
        max_length=settings.LEN_OGRN,
        validators=[validate_ogrn],
        unique=True,
        blank=False,
        verbose_name='ОГРН',
    )
    phone = models.CharField(
        validators=[validate_phone_number],
        max_length=settings.LEN_PHONE,
        blank=False,
        verbose_name='Телефон',
    )
    about = models.TextField(
        verbose_name='Об организации',
        max_length=settings.MAX_LEN_ABOUT_US,
        blank=True,
        validators=[validate_about],
    )
    city = models.ForeignKey(
        City,
        blank=False,
        on_delete=models.CASCADE,
        related_name='organization',
        verbose_name='Город',
    )
    photo = models.ImageField(
        blank=True,
        verbose_name='Фото',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return settings.ORGANIZATION.format(self.title, self.ogrn, self.city)


class Volunteer(models.Model):
    """
    Модель представляет собой информацию о волонтере.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='volunteers',
        verbose_name='Пользователь',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='volunteers',
        verbose_name='Город',
    )
    telegram = models.CharField(
        max_length=settings.MAX_LEN_TELEGRAM,
        blank=True,
        validators=[validate_telegram],
    )
    skills = models.ManyToManyField(
        Skills,
        through='VolunteerSkills',
        related_name='volunteers',
        verbose_name='Навыки',
    )
    photo = models.ImageField(
        blank=True,
        verbose_name='Фото',
    )
    date_of_birth = models.DateField(
        blank=False,
        null=False,
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),
            MaxValueValidator(limit_value=date.today()),
        ],
        verbose_name='Дата рождения',
        help_text='Введите дату в формате "ГГГГ-ММ-ДД", пример: "2000-01-01".',
    )
    phone = models.CharField(
        validators=[validate_phone_number],
        max_length=settings.LEN_PHONE,
        blank=True,
        verbose_name='Телефон',
    )

    class Meta:
        ordering = ['user__last_name']
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'

    def __str__(self):
        return settings.VOLUNTEER.format(self.user, self.city, self.skills)


class VolunteerSkills(models.Model):
    """
    Модель представляет собой список навыков волонтеров.
    """

    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('volunteer', 'skill'),
                name='unique_volunteer_skills',
            ),
        )

    def __str__(self):
        return f'{self.volunteer} {self.skill}'


class Category(models.Model):
    """
    Модель представляет собой категории проекта.
    """

    name = models.CharField(
        max_length=settings.MAX_LEN_NAME,
        verbose_name='Название',
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.MAX_LEN_SLUG,
        verbose_name='Слаг',
    )
    description = models.TextField(
        blank=False,
        verbose_name='Описание',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    Адрес проведения проекта.
    """

    address_line = models.CharField(
        max_length=100, verbose_name='Адрес в одну строчку'
    )
    street = models.CharField(max_length=75, verbose_name='Улица')
    house = models.CharField(max_length=5, verbose_name='Дом')
    block = models.CharField(
        max_length=5, blank=True, null=True, verbose_name='Корпус'
    )
    building = models.CharField(
        max_length=5, blank=True, null=True, verbose_name='Строение'
    )

    class Meta:
        verbose_name = 'Адрес проекта'
        verbose_name_plural = 'Адреса проектов'

    def __str__(self):
        return self.address_line


class Project(models.Model):
    """
    Модель представляет собой информацию о проекте.
    """

    APPROVED = 'approved'
    EDITING = 'editing'
    PENDING = 'pending'
    REJECTED = 'rejected'
    CANCELED_BY_ORGANIZER = 'canceled_by_organizer'
    OPEN = 'open'
    READY_FOR_FEEDBACK = 'ready_for_feedback'
    RECEPTION_OF_RESPONSES_CLOSED = 'reception_of_responses_closed'
    PROJECT_COMPLETED = 'project_completed'

    STATUS_CHOICES = [
        (APPROVED, 'Одобрено'),
        (EDITING, 'Черновик'),
        (PENDING, 'На рассмотрении'),
        (REJECTED, 'Отклонено'),
        (CANCELED_BY_ORGANIZER, 'Отменено организатором'),
    ]

    name = models.CharField(
        max_length=settings.MAX_LEN_NAME_PROJECT,
        validators=[validate_name],
        verbose_name='Название',
        unique=True,
    )
    description = models.TextField(
        blank=True,  # добавила
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V2,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Описание',
    )
    picture = models.ImageField(
        # blank=True,   #  добавилено для черновика
        # null=True,   #  добавила
        verbose_name='Картинка',
    )
    start_datetime = models.DateTimeField(
        blank=True,  # добавилено для черновика
        null=True,
        verbose_name='Дата и время, начало мероприятия',
    )
    end_datetime = models.DateTimeField(
        blank=True,  # добавилено для черновика
        null=True,
        verbose_name='Дата и время, окончания мероприятия',
    )
    start_date_application = models.DateTimeField(
        blank=True,  # добавилено для черновика
        null=True,
        verbose_name='Дата и время, начало подачи заявок',
    )
    end_date_application = models.DateTimeField(
        blank=True,  # добавилено для черновика
        null=True,
        verbose_name='Дата и время, окончания подачи заявок',
    )
    event_purpose = models.TextField(
        blank=True,  # добавилено для черновика
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V2,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Цель проекта',
    )
    event_address = models.ForeignKey(
        Address,
        blank=True,  # добавилено для черновика
        null=True,  # добавила
        on_delete=models.CASCADE,
        verbose_name='Адрес проведения проекта',
    )
    project_tasks = models.TextField(
        blank=True,  # добавилено для черновика
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V1,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Задачи проекта',
    )
    project_events = models.TextField(
        blank=True,  # добавилено для черновика
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V1,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Мероприятия на проекте',
    )
    organizer_provides = models.TextField(
        blank=True,
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V1,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Организатор предоставляет',
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Организация',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='project',
        blank=True,  # добавила
        null=True,  # если убрать null=True,то админка не показывает
        #  проект с пустым городами
        verbose_name='Город',
    )
    categories = models.ManyToManyField(
        Category,
        related_name='projects',
        # blank=True,  # добавила
        verbose_name='Категории',
    )
    photo_previous_event = models.ImageField(
        blank=True,
        # null=True,
        verbose_name='Фото с мероприятия',
    )
    participants = models.ManyToManyField(
        'ProjectParticipants',
        blank=True,
        related_name='projects',
        verbose_name='Участники',
    )
    status_approve = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name='Статус проверки',
    )
    skills = models.ManyToManyField(
        Skills,
        through='ProjectSkills',
        related_name='projects',
        # blank=True,  # добавила
        verbose_name='Навыки',
    )
    admin_comments = models.TextField(
        blank=True,
        validators=[
            regex_string_validator,
            LengthValidator(
                min_length=settings.MIN_LEN_TEXT_FIELD_V1,
                max_length=settings.MAX_LEN_TEXT_FIELD,
            ),
        ],
        verbose_name='Комментарии администратора',
    )

    class Meta:
        ordering = ('start_datetime',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return settings.PROJECT.format(
            self.name, self.organization, self.categories, self.city
        )


class ProjectCategories(models.Model):
    """
    Модель представляет собой список категорий проекта.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'project_category'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'category'],
                name='%(app_label)s%(class)s' '_unique_project_category',
            )
        ]
        verbose_name = 'Категория проекта'
        verbose_name_plural = 'Категории проекта'


class ProjectSkills(models.Model):
    """
    Модель представляет собой связь между проектом и навыками.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'project_skills'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'skill'],
                name='%(app_label)s%(class)s' '_unique_project_skills',
            )
        ]
        verbose_name = 'Навык проекта'
        verbose_name_plural = 'Навыки проекта'


class ProjectParticipants(models.Model):
    """
    Модель представляет собой список участников(волонтеров) проекта.
    """

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='participant'
    )
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'projects_volunteers'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'volunteer'],
                name='%(app_label)s%(class)s' '_unique_project_volunteer',
            )
        ]
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'

    def __str__(self):
        return settings.PROJECTPARTICIPANTS.format(
            self.project, self.volunteer
        )


class ProjectIncomes(models.Model):
    """
    Модель представляет собой заявки волонтеров на участие в проекте.
    """

    APPLICATION_SUBMITTED = 'application_submitted'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'

    STATUS_INCOMES = [
        (APPLICATION_SUBMITTED, 'Заявка подана'),
        (REJECTED, 'Отклонена'),
        (ACCEPTED, 'Принята'),
    ]
    project = models.ForeignKey(
        Project,
        blank=False,
        on_delete=models.CASCADE,
        related_name='project_incomes',
        verbose_name='Проект',
    )
    volunteer = models.ForeignKey(
        Volunteer,
        blank=False,
        on_delete=models.CASCADE,
        related_name='project_incomes',
        verbose_name='Волонтер',
    )
    status_incomes = models.CharField(
        max_length=100,
        choices=STATUS_INCOMES,
        default=APPLICATION_SUBMITTED,
        verbose_name='Статус заявки волонтера',
    )
    phone = models.CharField(
        validators=[validate_phone_number],
        max_length=settings.LEN_PHONE,
        blank=True,
        verbose_name='Телефон',
    )
    telegram = models.CharField(
        max_length=settings.MAX_LEN_TELEGRAM,
        blank=True,
        validators=[validate_telegram],
        verbose_name='Телеграм',
    )
    cover_letter = models.TextField(
        verbose_name='Сопроводительное письмо',
        blank=True,
        null=True,
        validators=[validate_about],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Статус заявки волонтера',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'volunteer', 'status_incomes'],
                name='%(app_label)s%(class)s_unique_project_volunteer',
            )
        ]
        verbose_name = 'Заявки волонтеров'
        verbose_name_plural = 'Заявки волонтеров'

    def __str__(self):
        return settings.PROJECTINCOMES.format(
            self.project, self.volunteer, self.status_incomes
        )


class VolunteerFavorite(models.Model):
    """
    Модель избранных проектов волонтеров.
    """

    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('volunteer', 'project'),
                name='unique_volunteer_favorites',
            ),
        )

    def __str__(self):
        return f'{self.volunteer} {self.project}'
