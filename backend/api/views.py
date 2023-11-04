import requests
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
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
    IsOrganizer,
    IsOrganizerOfProject,
    IsVolunteer,
    IsVolunteerOfIncomes,
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
    ProjectGetSerializer,
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
    # serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    permission_classes = [IsOrganizer]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProjectGetSerializer
        return ProjectSerializer

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
        permission_classes=(IsVolunteer,),
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


class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + f"/api/auth/activation/{uid}/{token}/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        if result.status_code == 204:
            return Response(status=result.status_code)
        else:
            return Response(result.json(), status=result.status_code)


class ProjectIncomesViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Представление для заявок волонтеров в рамках проектов.
    """

    queryset = ProjectIncomes.objects.all()
    serializer_class = ProjectIncomesSerializer
    # permission_classes = [IsVolunteer]

    @permission_classes([IsVolunteer])
    def create(self, request):
        """
        Создает новую заявку волонтера для участия в проекте.

        Parameters: pk (int): Идентификатор проекта, для которого
        создается заявка.
        Возвращает успешный ответ с сообщением о создании заявки.
        """
        project = self.get_object()
        serializer = self.get_serializer(
            data={
                'project': project.id,
                'volunteer': request.user.volunteer.id,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.data
        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsVolunteerOfIncomes],
    )
    def delete_incomes(self, request, pk):
        """
        Удаляет заявку волонтера на участие в проекте.

        Parameters: pk (int): Идентификатор заявки волонтера.
        Возвращает успешный ответ с сообщением о том, что заявка удалена.
        Если удалить не получилось, возвращает исключение.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.delete(instance)
        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsOrganizerOfProject],
    )
    def accept_incomes(self, request, pk):
        """
        Принимает заявку волонтера и добавляет его в участники проекта.

        Parameters: pk (int): Идентификатор заявки волонтера.
        Возвращает успешный ответ с сообщением о том, что заявка волонтера
        была принята и он добавлен в участники проекта.
        Если пользователь не является организатором проекта или заявка
        волонтера не принадлежит данному проекту вернется исключение.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.accept_incomes(instance)
        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['put'],
        permission_classes=[IsOrganizerOfProject],
    )
    def reject_incomes(self, request, pk):
        """
        Отклоняет заявку волонтера.

        Parameters: pk (int): Идентификатор заявки волонтера.
        Возвращает успешный ответ с сообщением о том, что заявка
        волонтера была отклонена.
        Если пользователь не является организатором проекта или заявка
        волонтера не принадлежит данному проекту вернется исключение.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.reject_incomes(instance)
        return Response(response_data, status=status.HTTP_200_OK)


class ProjectMeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Представление позволяет авторизованным пользователям с ролью
    Волонтер или Организатор просматривать свои проекты.
    """

    serializer_class = ProjectGetSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_class = ProjectMeFilter
    permission_classes = [IsOrganizer, IsVolunteer]

    def get_queryset(self):
        if self.request.user.is_volunteer:
            volunteer = get_object_or_404(Volunteer, user=self.request.user.id)
            from_volunteer_favorite = VolunteerFavorite.objects.filter(
                project=OuterRef('pk'),
                volunteer=volunteer
            )
            return (
                Project.objects
                .filter(participant__volunteer=volunteer)
                # .select_related('organization')
                # .prefetch_related('categories', 'skills')
                .annotate(
                    is_favorited=Exists(from_volunteer_favorite),
                )
            )
        if self.request.user.is_organizer:
            organization = get_object_or_404(
                Organization,
                contact_person=self.request.user.id
            )
            return Project.objects.filter(organization=organization)
