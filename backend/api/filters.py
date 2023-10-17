import django_filters
from django_filters.rest_framework import FilterSet

from projects.models import Project


class ProjectFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Project.STATUS_CHOICES)
    category = django_filters.CharFilter(lookup_expr='icontains')
    organizer = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'status', 'category', 'organizer']
