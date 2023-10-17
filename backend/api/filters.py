from django_filters.rest_framework import FilterSet, filters
# from django.core.validators import RegexValidator

from content.models import City, Skills
# from projects.models import Project
# from django.db.models import Q


class CityFilter(FilterSet):
    """Класс для фильтрации городов по имени."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = City
        fields = ('name', )


class SkillsFilter(FilterSet):
    """Класс для фильтрации навыков по имени."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Skills
        fields = ('name', )
