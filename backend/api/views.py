from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from backend.settings import VALUATIONS_ON_PAGE_ABOUT_US

from content.models import (City,
                            Feedback,
                            News,
                            PlatformAbout,
                            Valuation,
                            Skills
                            )
from projects.models import Project

from .filters import CityFilter, SkillsFilter
from .serializers import (
    FeedbackSerializer,
    NewsSerializer,
    PlatformAboutSerializer,
    PreviewNewsSerializer,
    ProjectSerializer,
    CitySerializer,
    SkillsSerializer
)


class PlatformAboutView(generics.RetrieveAPIView):
    serializer_class = PlatformAboutSerializer

    def get_object(self):
        platform_about = PlatformAbout.objects.latest('id')
        valuations = Valuation.objects.all()[:VALUATIONS_ON_PAGE_ABOUT_US]
        return {
            'about_us': platform_about.about_us,
            'platform_email': platform_about.platform_email,
            'valuations': valuations,
        }


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PreviewNewsSerializer
        return NewsSerializer


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_success_message(self, action, project_name):
        messages = {
            'create': f'Проект "{project_name}" успешно создан.',
            'update': f'Проект "{project_name}" успешно обновлен.',
            'destroy': f'Проект "{project_name}" успешно удален.',
        }
        return messages.get(action)

    @staticmethod
    def get_error_message(action, project_name):
        messages = {
            'create': f'Не удалось создать проект "{project_name}".',
            'update': f'Не удалось обновить проект "{project_name}".',
            'destroy': f'Не удалось удалить проект "{project_name}".',
        }
        return messages.get(action)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            project_name = serializer.validated_data.get('name')
            return Response(
                {'message': self.get_success_message('create', project_name)},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                'message': self.get_error_message(
                    'create', request.data.get('name')
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        project_name = instance.name
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {'message': self.get_success_message('update', project_name)}
            )
        return Response(
            {'message': self.get_error_message('update', project_name)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': self.get_success_message('destroy', instance.name)},
            status=status.HTTP_204_NO_CONTENT,
        )


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
    filterset_class = CityFilter


class SkillsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = None
    filterset_class = SkillsFilter
