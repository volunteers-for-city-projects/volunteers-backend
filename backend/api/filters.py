import django_filters
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import FilterSet, filters
from rest_framework.exceptions import ParseError
from taggit.models import Tag

from content.models import City, Skills
from projects.models import Category, Project, ProjectIncomes


class ProjectCategoryFilter(FilterSet):
    """
    Класс для фильтрации городов по имени.
    """

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ('name',)


class CityFilter(FilterSet):
    """
    Класс для фильтрации городов по имени.
    """

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = City
        fields = ('name',)


class SkillsFilter(FilterSet):
    """
    Класс для фильтрации навыков по имени.
    """

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Skills
        fields = ('name',)


class TagFilter(FilterSet):
    """
    Класс для фильтрации тегов по имени.
    """

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ('name',)


class ProjectFilter(FilterSet):
    """
    Класс для фильтрации проектов по имени, статусу, категории, организации.

    Примеры использования фильтров в URL:
    - /projects/?categories={id_categories}
    - /projects/?skills={id_skill}
    - /projects/?city={id_city}
    - /projects/?start_datetime=01.01.2023
    - /projects/?end_datetime=31.12.2023
    """

    categories = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='categories',
        to_field_name='id',
        # conjoined=True
    )

    skills = filters.ModelMultipleChoiceFilter(
        queryset=Skills.objects.all(),
        field_name='skills',
        to_field_name='id',
        # conjoined=True,  # все указанные навыки должны быть одновременно в проекте
    )

    city = django_filters.CharFilter(field_name='city', lookup_expr='exact')
    start_datetime = django_filters.DateTimeFilter(
        field_name='start_datetime', lookup_expr='gte'
    )
    end_datetime = django_filters.DateTimeFilter(
        field_name='end_datetime', lookup_expr='lte'
    )

    def filter_queryset(self, queryset):
        for name, value in self.data.items():
            try:
                queryset = super().filter_queryset(queryset)
            except (ValueError, self.Meta.model.DoesNotExist):
                raise ParseError("Invalid filter value for {}".format(name))

        return queryset

    class Meta:
        model = Project
        fields = [
            'categories',
            'skills',
            'city',
            'start_datetime',
            'end_datetime',
        ]


class StatusProjectFilter(django_filters.FilterSet):
    """
    Фильтр статусов для проектов в личном кабинете.

    Организатор может фильтровать проекты по одному из фильтров:
    по фильтру "Черновик" /projects/me/?draft=true,
    по фильтру "Активен" /projects/me/?active=true,
    по фильтру "Завершен" /projects/me/?completed=true,
    по фильтру "Архив" /projects/me/?archive=true,
    по фильтру "На модерации" /projects/me/?moderation=true,
    по фильтру "Избранное" /projects/me/?is_favorited=true.

    Волонтер может фильтровать проекты по одному из фильтров:
    по фильтру "Активен" /projects/me/?active=true,
    по фильтру "Завершен" /projects/me/?completed=true,
    по фильтру "Отменен" /projects/me/?archive=true,
    по фильтру "Избранное" /projects/me/?is_favorited=true.
    """

    def filter_draft(self, queryset):
        """
        Фильтр для таба "Черновик".
        """
        return queryset.filter(
            Q(status_approve__in=[Project.EDITING, Project.REJECTED,]),
            organization__contact_person=self.request.user
        )

    def filter_active(self, queryset):
        """
        Фильтр для таба "Активен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve=Project.APPROVED), end_datetime__gt=now,
            organization__contact_person=self.request.user
        )

    def filter_completed(self, queryset):
        """
        Фильтр для таба "Завершен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve=Project.APPROVED), end_datetime__lte=now,
            organization__contact_person=self.request.user
        )

    def filter_archive(self, queryset):
        """
        Фильтр для таба "Архив".
        """

        return queryset.filter(
            Q(status_approve=Project.CANCELED_BY_ORGANIZER),
            organization__contact_person=self.request.user
        )

    def filter_moderation(self, queryset):
        """
        Фильтр для таба "На модерации".
        """

        return queryset.filter(
            Q(status_approve=Project.PENDING),
            organization__contact_person=self.request.user
        )

    def filter_is_favorited(self, queryset):
        """
        Фильтр для таба "Избранные".
        """

        return queryset.filter(Q(project_favorite__user=self.request.user))

    def filter_active_volunteer(self, queryset):
        """
        Фильтр для таба "Активен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve=Project.APPROVED), end_datetime__gt=now,
            participants__volunteer=self.request.user.volunteers
        )

    def filter_completed_volunteer(self, queryset):
        """
        Фильтр для таба "Завершен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve=Project.APPROVED), end_datetime__lte=now,
            participants__volunteer=self.request.user.volunteers
        )

    def filter_archive_volunteer(self, queryset):
        """
        Фильтр для таба "Архив".
        """

        return queryset.filter(
            Q(status_approve=Project.CANCELED_BY_ORGANIZER),
            participants__volunteer=self.request.user.volunteers
        )

    def filter_queryset(self, queryset):
        user = self.request.user
        status_filter = None

        if user.is_organizer:
            status_filter = (
                self.data.get('draft') and self.filter_draft
                or self.data.get('active') and self.filter_active
                or self.data.get('completed') and self.filter_completed
                or self.data.get('archive') and self.filter_archive
                or self.data.get('moderation') and self.filter_moderation
                or self.data.get('is_favorited') and self.filter_is_favorited
            )
        elif user.is_volunteer:
            status_filter = (
                self.data.get('active')
                and self.filter_active_volunteer
                or self.data.get('completed')
                and self.filter_completed_volunteer
                or self.data.get('archive')
                and self.filter_archive_volunteer
                or self.data.get('is_favorited')
                and self.filter_is_favorited
            )

        if status_filter:
            queryset = status_filter(queryset).distinct()

        return queryset

    class Meta:
        model = Project
        fields = []


class ProjectIncomesFilter(django_filters.FilterSet):
    """
    Фильтр заявок по id Проекта.

    Пример фильтра /api/incomes/?project_id=1
    """

    project_id = django_filters.NumberFilter(field_name='project__id')

    class Meta:
        model = ProjectIncomes
        fields = ['project_id']
