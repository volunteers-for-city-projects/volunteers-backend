from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from taggit.models import Tag

from backend.settings import VALUATIONS_ON_PAGE_ABOUT_US
from content.models import (
    City,
    Feedback,
    News,
    PlatformAbout,
    Skills,
    Valuation,
)
from projects.models import Category, Organization, Project, Volunteer

from .filters import (
    CityFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    SkillsFilter,
    TagFilter,
)
from .permissions import IsOrganizerPermission
from .serializers import (
    CitySerializer,
    FeedbackSerializer,
    NewsSerializer,
    OgranizationCreateSerializer,
    OrganizationGetSerializer,
    OgranizationUpdateSerializer,
    PlatformAboutSerializer,
    PreviewNewsSerializer,
    ProjectCategorySerializer,
    ProjectSerializer,
    SkillsSerializer,
    TagSerializer,
    VolunteerCreateSerializer,
    VolunteerGetSerializer,
    VolunteerProfileSerializer,
    VolunteerUpdateSerializer,
)

# from taggit.serializers import TaggitSerializer


# from .filters import SearchFilter
# from django.db.models import Q


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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    permission_classes = [IsOrganizerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        if instance.organization.contact_person != request.user:
            message = "У вас нет разрешения на редактирование этой записи."
            return Response(
                {"detail": message}, status=status.HTTP_403_FORBIDDEN
            )
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        if instance.organization.contact_person != request.user:
            message = "У вас нет разрешения на удаление этой записи."
            return Response(
                {"detail": message}, status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VolunteerGetSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return VolunteerUpdateSerializer
        return VolunteerCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrganizationGetSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return OgranizationUpdateSerializer
        return OgranizationCreateSerializer


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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filterset_class = TagFilter


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ProjectCategorySerializer
    pagination_class = None
    filterset_class = ProjectCategoryFilter


class SearchListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_class = SearchFilter
    search_fields = ['name', 'description', 'event_purpose']


# class VolunteerProfileView(generics.RetrieveAPIView):
#     queryset = Volunteer.objects.all()
#     serializer_class = VolunteerProfileSerializer


#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs['pk']
#         try:
#             volunteer = self.get_queryset().get(pk=pk)
#             serializer = self.get_serializer(volunteer)
#             return Response(serializer.data)
#         except Volunteer.DoesNotExist:
#             return Response({'error': 'Волонтер не найден'}, status=404)


class VolunteerProfileView(generics.RetrieveAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerProfileSerializer
