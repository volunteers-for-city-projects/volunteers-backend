from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from taggit.models import Tag

from api import schemas
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
    StatusProjectFilter,
    TagFilter,
)
from .mixins import DestroyUserMixin
from .permissions import (
    IsOrganizer,
    IsOrganizerOfProject,
    IsOrganizerOrReadOnly,
    IsOwnerOrganization,
    IsOwnerVolunteer,
    IsVolunteer,
    IsVolunteerOfIncomes,
)
from .serializers import (
    CitySerializer,
    DraftProjectSerializer,
    FeedbackSerializer,
    NewsSerializer,
    OgranizationCreateSerializer,
    OgranizationUpdateSerializer,
    OrganizationGetSerializer,
    PlatformAboutSerializer,
    PreviewNewsSerializer,
    ProjectCategorySerializer,
    ProjectGetSerializer,
    ProjectIncomesGetSerializer,
    ProjectIncomesSerializer,
    ProjectSerializer,
    SkillsSerializer,
    TagSerializer,
    VolunteerCreateSerializer,
    VolunteerFavoriteGetSerializer,
    VolunteerGetSerializer,
    VolunteerUpdateSerializer,
)

# from backend.api import permissions

# from taggit.serializers import TaggitSerializer

# from .filters import SearchFilter
# from django.db.models import Q


class PlatformAboutView(generics.RetrieveAPIView):
    """
    Отображает информацию о Платформе.

    Любой пользователь может получить информацию о нас,
    ценностях и email Платформы.

    """

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
    """
    Представление для новостей.

    Позволяет просматривать новости списком и по отдельности.
    """

    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PreviewNewsSerializer
        return NewsSerializer


class FeedbackCreateView(generics.CreateAPIView):
    """
    Представление для обращений.

    Позволяет пользователям отправлять обращение
    администратору платформы.
    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Представление для проектов.

    Позволяет создавать, просматривать, обновлять и удалять проекты.
    Только авторизованные пользователи-организаторы, связанные с проектом
    в качестве контактных лиц, могут вносить изменения.
    """

    queryset = Project.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    permission_classes = [IsOrganizerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProjectGetSerializer
        if self.request.query_params.get('save_draft') == 'True':
            return DraftProjectSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        if instance.organization.contact_person != request.user:
            message = "У вас нет разрешения на редактирование этой записи."
            return Response(
                {"detail": message}, status=status.HTTP_403_FORBIDDEN
            )
        if instance.status_approve == Project.APPROVED and \
           instance.end_datetime < timezone.now():
            return Response(
                {"detail": "Вы не можете редактировать завершенные проекты"},
                status=status.HTTP_400_BAD_REQUEST
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
        """
        Удаляет проект.

        Удалить проект можно только организатору этого проекта и
        только со статусом в Архиве(Отменен организатором) или Черновик.
        """
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        if instance.organization.contact_person != request.user:
            message = "У вас нет разрешения на удаление этой записи."
            return Response(
                {"detail": message}, status=status.HTTP_403_FORBIDDEN
            )
        #  Проверяем статус проекта возможно нужно еще добавить какие то статусы
        if instance.status_approve not in [
            Project.EDITING, Project.CANCELED_BY_ORGANIZER
        ]:
            message = ('Вы не можете удалить проекты, '
                       'не находящиеся в архиве или в черновике.')
            return Response(
                {"detail": message}, status=status.HTTP_400_BAD_REQUEST
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


class VolunteerViewSet(DestroyUserMixin, viewsets.ModelViewSet):
    """
    Представление для волонтеров.

    Позволяет получать, создавать, редактировать, удалять участника-волонтера.
    """

    # permission_classes = (AllowAny,)
    queryset = Volunteer.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return VolunteerGetSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return VolunteerUpdateSerializer
        return VolunteerCreateSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsOwnerVolunteer,)
        else:
            self.permission_classes = (AllowAny,)

        return super(VolunteerViewSet, self).get_permissions()


class OrganizationViewSet(DestroyUserMixin, viewsets.ModelViewSet):
    """
    Представление для орагизаций - организаторов проекта.

    Позволяет получать, создавать, редактировать,
    удалять организацию-организатора проекта.
    """

    # permission_classes = (AllowAny,)
    queryset = Organization.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OrganizationGetSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return OgranizationUpdateSerializer
        return OgranizationCreateSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            self.permission_classes = (IsOwnerOrganization,)
        else:
            self.permission_classes = (AllowAny,)

        return super(OrganizationViewSet, self).get_permissions()


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для отображения городов.

    ---
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
    filterset_class = CityFilter


class SkillsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для отображения навыков.

    ---
    """

    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    pagination_class = None
    filterset_class = SkillsFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для отображения тегов.

    ---
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filterset_class = TagFilter


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для отображения категорий проекта.

    ---
    """

    queryset = Category.objects.all()
    serializer_class = ProjectCategorySerializer
    pagination_class = None
    filterset_class = ProjectCategoryFilter


class SearchListView(generics.ListAPIView):
    """
    Представление для отображения строки поиска.

    ---
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_class = SearchFilter
    search_fields = ['name', 'description', 'event_purpose']


class ProjectIncomesViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """
    Представление для заявок волонтеров в рамках проектов.

    ---
    """

    queryset = ProjectIncomes.objects.all()
    permission_classes = [IsOrganizerOfProject]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_organizer:
            return ProjectIncomes.objects.filter(
                project__organization__contact_person=user
            )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProjectIncomesGetSerializer
        return ProjectIncomesSerializer

    def get_permissions(self):
        """
        Метод для установки разрешений в зависимости от действия.
        """
        permission_classes_by_action = {
            'list': [IsOrganizerOfProject],
            'create': [IsVolunteer],
            'accept_incomes': [IsOrganizerOfProject],
            'reject_incomes': [IsOrganizerOfProject],
            'delete_incomes': [IsVolunteerOfIncomes],
            'retrieve': [IsOrganizerOfProject | IsVolunteerOfIncomes],
        }
        permission_classes = permission_classes_by_action.get(
            self.action, [IsOrganizerOfProject]
        )
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
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

    @action(detail=True, methods=['post'])
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

    @action(detail=True, methods=['put'])
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
    Отображает проекты текущего пользователя.

    Представление позволяет авторизованным пользователям с ролью
    Волонтер или Организатор просматривать свои проекты.
    """

    serializer_class = ProjectGetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StatusProjectFilter
    permission_classes = [IsOrganizer | IsVolunteer]

    def get_queryset(self):
        if self.request.user.is_volunteer:
            volunteer = get_object_or_404(Volunteer, user=self.request.user.id)
            from_volunteer_favorite = VolunteerFavorite.objects.filter(
                project=OuterRef('pk'), volunteer=volunteer
            )
            return (
                Project.objects.filter(participant__volunteer=volunteer)
                # .select_related('organization')
                # .prefetch_related('categories', 'skills')
                .annotate(
                    is_favorited=Exists(from_volunteer_favorite),
                )
            )

        if self.request.user.is_organizer:
            return Project.objects.filter(
                organization__contact_person=self.request.user
            )
            # organization = get_object_or_404(
            #     Organization,
            #     contact_person=self.request.user.id
            # )
            # return Project.objects.filter(organization=organization)

        #  добавила иначе ошибка если заходить администратором
        # raise PermissionDenied(
        #     detail='Вы не являетесь волонтером или организатором'
        # )

    @swagger_auto_schema(
        manual_parameters=schemas.status_project_filter_params
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
