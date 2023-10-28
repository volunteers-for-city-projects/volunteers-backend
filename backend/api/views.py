from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
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
from projects.models import (
    Category,
    Organization,
    Project,
    ProjectIncomes,
    ProjectParticipants,
    Volunteer,
    VolunteerFavorite,
)

from .filters import (
    CityFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    SkillsFilter,
    TagFilter,
)
from .permissions import (
    IsOrganizerPermission,
    IsOwnerOrReadOnlyPermission,
    IsVolunteerPermission,
)
from .serializers import (
    CitySerializer,
    FeedbackSerializer,
    NewsSerializer,
    OgranizationCreateSerializer,
    OgranizationUpdateSerializer,
    OrganizationGetSerializer,
    PlatformAboutSerializer,
    PreviewNewsSerializer,
    ProjectCategorySerializer,
    ProjectIncomesSerializer,
    ProjectSerializer,
    SkillsSerializer,
    TagSerializer,
    VolunteerCreateSerializer,
    VolunteerFavoriteGetSerializer,
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
    """
    Представление для проектов.

    Позволяет создавать, просматривать, обновлять и удалять проекты.
    Только авторизованные пользователи-организаторы, связанные с проектом
    в качестве контактных лиц, могут вносить изменения.
    """

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

    def add_to(self, volunteer, project, errors):
        """
        Добавить проект в избранное.
        """
        _, created = VolunteerFavorite.objects.get_or_create(
            volunteer=volunteer, project=project
        )
        if not created:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = VolunteerFavoriteGetSerializer(instance=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, volunteer, project, errors):
        """
        Удалить проект из избранного.
        """
        cnt_deleted, _ = VolunteerFavorite.objects.filter(
            volunteer=volunteer, project=project
        ).delete()

        if cnt_deleted == 0:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsVolunteerPermission,),
    )
    def favorite(self, request, **kwargs):
        """
        Избранные проекты волонтера.
        """
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        volunteer = get_object_or_404(Volunteer, user=request.user)
        if request.method == 'POST':
            return self.add_to(
                volunteer, project, 'Данный проект уже есть в избранном!'
            )
        return self.delete_from(
            volunteer, project, 'Данного проекта нет в избранном!'
        )


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


class VolunteerProfileView(generics.RetrieveAPIView):
    """
    Представление для получения профиля волонтера (личный кабинет волонтера).

    Позволяет волонтерам получать свой собственный профиль. Доступно только
    авторизованным волонтерам.
    """

    queryset = Volunteer.objects.all()
    serializer_class = VolunteerProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        volunteer = self.get_object()
        if volunteer.user != request.user:
            return Response(
                {'error': 'Недостаточно прав доступа'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(volunteer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectIncomesView(generics.CreateAPIView):
    queryset = ProjectIncomes.objects.all()
    serializer_class = ProjectIncomesSerializer
    permission_classes = [IsVolunteerPermission]


class ProjectIncomesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectIncomes.objects.all()
    serializer_class = ProjectIncomesSerializer
    permission_classes = [IsOwnerOrReadOnlyPermission]
