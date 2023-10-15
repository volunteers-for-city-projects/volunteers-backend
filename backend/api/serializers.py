from rest_framework import serializers

from content.models import News
from projects.models import Project


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'picture',
            'start_datatime',
            'end_datatime',
            'application_date',
            'event_purpose',
            'organization',
            'city',
            'category',
            'status_project',
            'photo_previous_event',
            'participants',
            'status_approve',
        )
