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
    organizer = django_filters.NumberFilter(
        field_name='organization', lookup_expr='exact'
    )

    class Meta:
        model = Project
        fields = ['name', 'category', 'organizer']


class StatusProjectOrganizerFilter(django_filters.FilterSet):
    """
    Фильтр статусов для проектов в личном кабинете организатора.
    """

    # Фильтр для таба "Черновик"
    draft = django_filters.CharFilter(method='filter_draft')

    # Фильтр для таба "Активен"
    active = django_filters.CharFilter(method='filter_active')

    # Фильтр для таба "Завершен"
    completed = django_filters.CharFilter(method='filter_completed')

    # Фильтр для таба "Архив"
    archive = django_filters.CharFilter(method='filter_archive')

    def filter_draft(self, queryset, name, value):
        return queryset.filter(
            Q(status_approve__in=['editing', 'rejected', 'pending'])
        )

    def filter_active(self, queryset, name, value):
        now = timezone.now()
        return queryset.filter(
            Q(status_approve='approved'), end_datetime__gt=now
        )

    def filter_completed(self, queryset, name, value):
        now = timezone.now()
        return queryset.filter(
            Q(status_approve='approved'), end_datetime__lte=now
        )

    def filter_archive(self, queryset, name, value):
        return queryset.filter(Q(status_approve='canceled_by_organizer'))

    class Meta:
        model = Project
        fields = []


# /projects/me/?active=true
# /projects/me/?draft=true


class StatusProjectVolunteerFilter(django_filters.FilterSet):
    """
    Фильтр статусов для проектов в личном кабинете волонтера.
    """

    pass
