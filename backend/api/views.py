# from django.shortcuts import render
from rest_framework import viewsets

from content.models import News
from projects.models import Project

from .serializers import NewsSerializer, ProjectSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
