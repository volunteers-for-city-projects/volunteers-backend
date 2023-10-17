import django_filters
from django_filters.rest_framework import FilterSet, filters

# from django.core.validators import RegexValidator

from content.models import City, Skills
from projects.models import Project

# from django.db.models import Q


class CityFilter(FilterSet):
    """Класс для фильтрации городов по имени."""

    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = City
        fields = ('name',)


class SkillsFilter(FilterSet):
    """Класс для фильтрации навыков по имени."""

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Skills
        fields = ('name',)


class ProjectFilter(FilterSet):
    """
    Класс для фильтрации проектов по имени, статусу, категории, организации.
    """

    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Project.STATUS_CHOICES)
    category = django_filters.CharFilter(lookup_expr='icontains')
    organizer = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'status', 'category', 'organizer']
