import django_filters
from django_filters.rest_framework import FilterSet, filters
from taggit.models import Tag

from content.models import City, Skills
from projects.models import Category, Project

# from django.core.validators import RegexValidator
# from django.db.models import Q


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
    status = django_filters.ChoiceFilter(
        field_name='status_project', choices=Project.STATUS_PROJECT
    )
    category = django_filters.CharFilter(
        field_name='category', lookup_expr='exact'
    )
    organizer = django_filters.NumberFilter(
        field_name='organization', lookup_expr='exact'
    )

    class Meta:
        model = Project
        fields = ['name', 'status', 'category', 'organizer']
