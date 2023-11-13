import django_filters
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import FilterSet, filters
from taggit.models import Tag

from content.models import City, Skills
from projects.models import Category, Project


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
    """

    name = django_filters.CharFilter(lookup_expr='icontains')
    # TODO: Пересмотреть логику статусов проекта,
    # текущая реализация не актуальная.
    # status = django_filters.ChoiceFilter(
    #     field_name='status_project', choices=Project.STATUS_PROJECT
    # )
    category = django_filters.CharFilter(
        field_name='category', lookup_expr='exact'
    )
    skills = django_filters.CharFilter(
        field_name='skills', lookup_expr='exact'
    )
    organizer = django_filters.NumberFilter(
        field_name='organization', lookup_expr='exact'
    )
    city = django_filters.CharFilter(
        field_name='city__name', lookup_expr='icontains'
    )
    start_datetime = django_filters.DateTimeFilter(
        field_name='start_datetime', lookup_expr='gte'
    )
    end_datetime = django_filters.DateTimeFilter(
        field_name='end_datetime', lookup_expr='lte'
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'category',
            'skills',
            'organizer',
            'city',
            'start_datetime',
            'end_datetime',
        ]


class StatusProjectFilter(django_filters.FilterSet):
    """
    Фильтр статусов для проектов в личном кабинете.

    Организатор может фильтровать проекты по одному из фильтров:
    по фильтру "Черновик" /projects/me/?draft=true
    по фильтру "Активен" /projects/me/?active=true
    по фильтру "Завершен" /projects/me/?completed=true
    по фильтру "Архив" /projects/me/?archive=true.

    Волонтер может фильтровать проекты по одному из фильтров:
    по фильтру "Активен" /projects/me/?active=true
    по фильтру "Завершен" /projects/me/?completed=true.
    """

    draft = django_filters.CharFilter(method='filter_draft')
    active = django_filters.CharFilter(method='filter_active')
    completed = django_filters.CharFilter(method='filter_completed')
    archive = django_filters.CharFilter(method='filter_archive')

    def filter_draft(self, queryset):
        """
        Фильтр для таба "Черновик".
        """
        return queryset.filter(
            Q(status_approve__in=['editing', 'rejected', 'pending'])
        )

    def filter_active(self, queryset):
        """
        Фильтр для таба "Активен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve='approved'), end_datetime__gt=now
        )

    def filter_completed(self, queryset):
        """
        Фильтр для таба "Завершен".
        """
        now = timezone.now()
        return queryset.filter(
            Q(status_approve='approved'), end_datetime__lte=now
        )

    def filter_archive(self, queryset):
        """
        Фильтр для таба "Архив".
        """
        return queryset.filter(Q(status_approve='canceled_by_organizer'))

    #  TODO фильтры по статусам проекта в ЛК Волонтера
    #  Простой код для понимания и дополнения статусов волнтеров
    # def filter_queryset(self, queryset):
    #     user = self.request.user
    #     if user.is_organizer:
    #         if self.data.get("draft"):
    #             queryset = self.filter_draft(queryset)
    #         elif self.data.get("active"):
    #             queryset = self.filter_active(queryset)
    #         elif self.data.get("completed"):
    #             queryset = self.filter_completed(queryset)
    #         elif self.data.get("archive"):
    #             queryset = self.filter_archive(queryset)
    #     elif user.is_volunteer:
    #         if self.data.get("active"):
    #             queryset = self.filter_active(queryset)
    #         elif self.data.get("completed"):
    #             queryset = self.filter_completed(queryset)
    #     return queryset

    def filter_queryset(self, queryset):
        user = self.request.user
        status_filter = None

        if user.is_organizer:
            status_filter = (
                self.data.get("draft")
                and self.filter_draft
                or self.data.get("active")
                and self.filter_active
                or self.data.get("completed")
                and self.filter_completed
                or self.data.get("archive")
                and self.filter_archive
            )
        elif user.is_volunteer:
            status_filter = (
                self.data.get("active")
                and self.filter_active
                or self.data.get("completed")
                and self.filter_completed
            )

        if status_filter:
            queryset = status_filter(queryset)

        return queryset

    class Meta:
        model = Project
        fields = []
