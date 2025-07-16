import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from taggit.models import Tag

from api.utils import NonEmptyBase64ImageField, create_user, get_site_data
from content.models import (
    City,
    Feedback,
    News,
    PlatformAbout,
    Skills,
    Valuation,
)
from notifications.tasks import (
    incomes_approve_send_email,
    incomes_reject_send_email,
)
from projects.models import (
    Address,
    Category,
    Organization,
    Project,
    ProjectFavorite,
    ProjectImage,
    ProjectIncomes,
    ProjectParticipants,
    Volunteer,
    VolunteerSkills,
)

from .mixins import IsValidModifyErrorForFrontendMixin
from .validators import validate_dates, validate_status_incomes

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения адреса.
    """

    class Meta:
        model = Address
        fields = '__all__'


class ValuationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ценностей платформы.
    """

    class Meta:
        model = Valuation
        fields = ('title', 'description')


class PlatformAboutSerializer(serializers.ModelSerializer):
    """
    Сериалзиатор для отображения информации о платформе.
    """

    valuations = ValuationSerializer(many=True)
    projects_count = serializers.SerializerMethodField()
    volunteers_count = serializers.SerializerMethodField()
    organizers_count = serializers.SerializerMethodField()

    class Meta:
        model = PlatformAbout
        fields = (
            'about_us',
            'platform_email',
            'valuations',
            'projects_count',
            'volunteers_count',
            'organizers_count',
        )

    def get_projects_count(self, obj):
        return Project.objects.filter(status_approve=Project.APPROVED).count()

    def get_volunteers_count(self, obj):
        return Volunteer.objects.count()

    def get_organizers_count(self, obj):
        return Organization.objects.count()


class TagListSerializerField(serializers.Serializer):
    """
    Возвращает список хештегов для новостей.
    """

    def to_representation(self, value):
        return [tag.name for tag in value.all()]


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра новости в детализации.
    """

    tags = TagListSerializerField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('picture', 'tags', 'title', 'text', 'author', 'created_at')

    def get_author(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'


class PreviewNewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра новостей списком.
    """

    tags = TagListSerializerField()

    class Meta:
        model = News
        fields = ('picture', 'title', 'tags', 'created_at')


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обращений.
    """

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'text')


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения городов.
    """

    class Meta:
        model = City
        fields = ('id', 'name')


class ProjectCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения категорий проекта.
    """

    class Meta:
        model = Category
        exclude = ('description',)


class SkillsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения навыков.
    """

    class Meta:
        model = Skills
        fields = ('id', 'name')


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ('id', 'project', 'photo')


class VolunteerGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения волонтера.
    """

    user = UserSerializer(read_only=True)
    skills = SkillsSerializer(many=True)

    class Meta:
        model = Volunteer
        fields = (
            'id',
            'user',
            'city',
            'telegram',
            'skills',
            'photo',
            'date_of_birth',
            'phone',
        )


class ProjectParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка участников.
    """
    volunteer = VolunteerGetSerializer()

    class Meta:
        model = ProjectParticipants
        fields = (
            'id',
            'volunteer',
        )


class ProjectGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных проекта.
    """

    event_address = AddressSerializer(read_only=True)
    skills = SkillsSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    city = serializers.SlugRelatedField(slug_field='name', read_only=True)
    photos = ProjectImageSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProjectFavorite.objects.filter(
                user=request.user,
                project=obj,
            ).exists()
        return False

    def get_status(self, data):
        OPEN = 'open'
        READY = 'ready_for_feedback'
        CLOSED = 'reception_of_responses_closed'
        COMPLETED = 'project_completed'
        CANCELED = 'canceled_by_organizer'
        EDITING = 'editing'

        if data.status_approve == Project.CANCELED_BY_ORGANIZER:
            return CANCELED
        elif data.status_approve == Project.APPROVED:
            now = timezone.now()
            if data.start_datetime <= now < data.start_date_application:
                return OPEN
            elif (
                data.start_date_application <= now < data.end_date_application
            ):
                return READY
            elif data.end_date_application <= now < data.end_datetime:
                return CLOSED
            elif data.end_datetime <= now:
                return COMPLETED
        return EDITING

    def get_participants(self, obj):
        participants_data = ProjectParticipantSerializer(
            obj.participants.all(), many=True
        ).data
        return [
            {
                'id': participant.get('id'),
                'volunteer_id': participant['volunteer']['id'],
                'full_name': (
                    f'{participant["volunteer"]["user"]["last_name"]} '
                    f'{participant["volunteer"]["user"]["first_name"]} '
                    f'{participant["volunteer"]["user"]["second_name"]}'
                )
            }
            for participant in participants_data
        ]

    class Meta:
        model = Project
        fields = (
            'id',
            'created_at',
            'name',
            'description',
            'picture',
            'start_datetime',
            'end_datetime',
            'start_date_application',
            'end_date_application',
            'event_purpose',
            'event_address',
            'project_tasks',
            'project_events',
            'organizer_provides',
            'organization',
            'city',
            'categories',
            'participants',
            'admin_comments',
            'status_approve',
            'skills',
            'is_favorited',
            'status',
            'photos'
        )
        read_only_fields = fields


class DraftProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/редоктирования черновика - проекта.
    """

    event_address = AddressSerializer(required=False, allow_null=True)
    skills = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Skills.objects.all(), many=True
    )
    picture = Base64ImageField(required=False, allow_null=True)

    def validate_status_approve(self, value):
        if value != Project.EDITING:
            raise serializers.ValidationError(
                'Вы передаете невверный статус для черновика.'
            )
        return value

    def create(self, validated_data):
        address_data = validated_data.pop('event_address', None)
        with transaction.atomic():
            project_instance = super().create(validated_data)
            project_instance.status_approve = Project.EDITING
            project_instance.save()
            if address_data:
                address, _ = Address.objects.get_or_create(**address_data)
                project_instance.event_address = address
                project_instance.save()
        return project_instance

    def update(self, instance, validated_data):
        status_approve = instance.status_approve
        if status_approve not in (Project.EDITING, Project.REJECTED):
            raise serializers.ValidationError(
                'Сохранять как черновик можно проекты  '
                f'со статусом {Project.EDITING} или {Project.REJECTED}.'
            )
        address_data = validated_data.pop('event_address', None)
        if address_data:
            address = instance.event_address
            if address:
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(**address_data)
                instance.event_address = address
        return super().update(instance, validated_data)

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'picture',
            'start_datetime',
            'end_datetime',
            'start_date_application',
            'end_date_application',
            'event_purpose',
            'event_address',
            'project_tasks',
            'project_events',
            'organizer_provides',
            'organization',
            'city',
            'categories',
            'status_approve',
            'skills',
        )
        read_only_fields = ('organization',)
        extra_kwargs = {
            'status_approve': {'required': False},
            'categories': {'required': False, 'allow_empty': True},
            'event_address': {'required': False, 'allow_empty': True},
        }


class ProjectSerializer(serializers.ModelSerializer):

    """
    Сериализатор для создания/редактирования проекта.
    """

    event_address = AddressSerializer()
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skills.objects.all(), many=True, allow_null=False
    )
    picture = NonEmptyBase64ImageField()
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=True,
        allow_null=False,  # Запретить отправку значения None. если удасться
        # убрать из модели null=True и чтоб не ломалась админка то можно
        #  удалить полностью city из сериализатор
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'picture',
            'start_datetime',
            'end_datetime',
            'start_date_application',
            'end_date_application',
            'event_purpose',
            'event_address',
            'project_tasks',
            'project_events',
            'organizer_provides',
            'organization',
            'city',
            'categories',
            'status_approve',
            'skills',
        )
        read_only_fields = ('organization',)
        extra_kwargs = {field: {'required': True} for field in fields}
        extra_kwargs = {
            'status_approve': {'required': False},
            'event_purpose': {'allow_blank': False, 'required': True},
            'project_tasks': {'allow_blank': False, 'required': True},
            'project_events': {'allow_blank': False, 'required': True},
            'organizer_provides': {'allow_blank': True, 'required': False},
            'description': {'allow_blank': False, 'required': True},
        }

    def validate_skills(self, value):
        if not value:
            raise serializers.ValidationError("Выберите хоть один навык.")
        return value

    def validate(self, data):
        try:
            start_datetime = data['start_datetime']
            end_datetime = data['end_datetime']
            start_date_application = data['start_date_application']
            end_date_application = data['end_date_application']
        except KeyError as field:
            raise serializers.ValidationError(
                f'{self.__class__.__name__}: Передайте в запросе поле {field}'
            )
        try:
            validate_dates(
                start_datetime,
                end_datetime,
                start_date_application,
                end_date_application,
            )
        except serializers.ValidationError as errors:
            raise serializers.ValidationError(
                {self.__class__.__name__: errors.detail}
            )
        return data

    def validate_status_approve(self, value):
        allowed_statuses = dict(Project.STATUS_CHOICES).keys()
        if value not in allowed_statuses:
            raise serializers.ValidationError(
                f"Вы передаете неподдерживаемый статус: {value}"
            )
        if self.instance is None and value != Project.PENDING:
            raise serializers.ValidationError(
                'Вы передаете неверный статус для создания проекта.'
            )
        return value

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        skills = validated_data.pop('skills')
        with transaction.atomic():
            address, _ = Address.objects.get_or_create(
                **validated_data.pop('event_address')
            )
            address.address_line = re.sub(' +', ' ', address.address_line)
            project_instanse = Project.objects.create(
                event_address=address, **validated_data
            )
            project_instanse.skills.set(skills)
            project_instanse.categories.set(categories)
        return project_instanse

    def update(self, instance, validated_data):
        address_data = validated_data.pop('event_address', None)
        if address_data:
            address = instance.event_address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.address_line = re.sub(' +', ' ', address.address_line)
            address.save()
        return super(ProjectSerializer, self).update(instance, validated_data)


class ActiveProjectEditSerializer(ProjectSerializer):
    """
    Сериализатор для частичного редактирования Активного проекта.
    """

    class Meta(ProjectSerializer.Meta):
        read_only_fields = ProjectSerializer.Meta.read_only_fields + (
            'description',
            'event_purpose',
            'event_address',
            'project_tasks',
            'project_events',
            'organizer_provides',
            'city',
            'categories',
            'skills',
        )

    def validate(self, data):
        status_approve = data.get('status_approve')
        if status_approve == 'canceled_by_organizer':
            return data
        else:
            return super().validate(data)


class ProjectCompleteSerializer(ProjectSerializer):
    """
    Сериализатор для добавления фото к Заверненным проектам.
    """
    photos = ProjectImageSerializer(many=True, read_only=True)
    uploaded_photos = serializers.ListField(
        max_length=settings.MAX_LEN_PHOTOS,
        child=Base64ImageField(
            max_length=20000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False
    )

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('photos', 'uploaded_photos',)
        read_only_fields = ProjectSerializer.Meta.fields

    def validate(self, data):
        return data

# если зазгрузка фоток не обязательная, иначе убрать  if uploaded_data:
    def update(self, instance, validated_data):
        uploaded_data = validated_data.pop('uploaded_photos', None)
        instance.photos.all().delete()
        if uploaded_data:
            for uploaded_photo in uploaded_data:
                ProjectImage.objects.create(
                    project=instance, photo=uploaded_photo
                )

        return super().update(instance, validated_data)


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения тегов.
    """

    class Meta:
        model = Tag
        fields = (
            'name',
            'slug',
        )


class VolunteerCreateSerializer(
    IsValidModifyErrorForFrontendMixin, serializers.ModelSerializer
):
    """
    Сериализатор для создания волонтера.
    """

    user = UserCreateSerializer()
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skills.objects.all(), many=True
    )
    photo = Base64ImageField(required=False)

    def create_skills(self, skills, volunteer):
        data = []
        for skill in skills:
            data.append(VolunteerSkills(volunteer=volunteer, skill=skill))
        VolunteerSkills.objects.bulk_create(data)

    @transaction.atomic
    def create(self, validated_data):
        skills = validated_data.pop('skills')
        user_data = validated_data.pop('user')

        user_data['role'] = User.VOLUNTEER

        user = create_user(self, UserCreateSerializer, user_data)
        volunteer = Volunteer.objects.create(user=user, **validated_data)
        self.create_skills(skills, volunteer)

        return volunteer

    class Meta:
        model = Volunteer
        fields = '__all__'


class VolunteerUpdateSerializer(VolunteerCreateSerializer):
    """
    Сериализатор для редактирования волонтера.
    """

    user = UserSerializer()

    @transaction.atomic
    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        VolunteerSkills.objects.filter(volunteer=instance).delete()
        self.create_skills(skills, instance)

        user_data = validated_data.pop('user')
        instance.user.first_name = user_data.get('first_name')
        instance.user.second_name = user_data.get('second_name')
        instance.user.last_name = user_data.get('last_name')
        instance.user.save()

        # Убираем из параметров дату рождения, если она указана в JSON явно:
        # в соответсвии с тербованиями редактирование запрещено
        if validated_data.get('date_of_birth') is not None:
            validated_data.pop('date_of_birth')

        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()
        return instance


class ProjectIncomesGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения данных о заявках волонтеров.
    """

    volunteer = VolunteerGetSerializer(read_only=True)
    project = ProjectGetSerializer(read_only=True)

    class Meta:
        model = ProjectIncomes
        fields = (
            'id',
            'project',
            'volunteer',
            'status_incomes',
            'created_at',
            'phone',
            'telegram',
            'cover_letter',
        )


class ProjectIncomesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заявок волонтеров.
    """

    class Meta:
        model = ProjectIncomes
        fields = (
            'id',
            'project',
            'volunteer',
            'status_incomes',
            'phone',
            'telegram',
            'cover_letter',
            'created_at',
        )
        read_only_fields = ('id', 'created_at', 'volunteer')

    def create(self, validated_data):
        """
        Создает заявку волонтера.
        """

        project = validated_data.get('project')
        volunteer = self.context['request'].user.volunteers
        status_incomes = validated_data.get(
            'status_incomes', ProjectIncomes.APPLICATION_SUBMITTED
        )
        if not (
            project.status_approve == Project.APPROVED and
            (project.start_date_application < timezone.now()
             < project.end_date_application)
        ):
            raise serializers.ValidationError(
                'Нельзя подать заявку на проект, '
                'к которому не открыта подача заявок.'
            )
        if (
            project.project_incomes.filter(volunteer=volunteer)
            .exclude(status_incomes=ProjectIncomes.REJECTED).exists()
        ):
            raise serializers.ValidationError(
                'Заявка волонтера на этот проект уже существует.'
            )
        if (
            project.project_incomes.filter(
                volunteer=volunteer, status_incomes=ProjectIncomes.REJECTED
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы не можете повторно подать завку, '
                'ваша заявка ранее была отклонена'
            )
        project_income = ProjectIncomes.objects.create(
            project=project,
            volunteer=volunteer,
            status_incomes=status_incomes,
            phone=validated_data.get('phone', ''),
            telegram=validated_data.get('telegram', ''),
            cover_letter=validated_data.get('cover_letter', ''),
        )
        return project_income

    def validate_status_incomes(self, value):
        return validate_status_incomes(value)

    def accept_incomes(self, instance):
        """
        Принимает заявку волонтера и добавляет его в участники проекта.
        """
        existing_participant = ProjectParticipants.objects.filter(
            project=instance.project, volunteer=instance.volunteer
        ).first()
        if existing_participant:
            raise serializers.ValidationError(
                'Этот волонтер уже является участником проекта.'
            )
        instance.status_incomes = ProjectIncomes.ACCEPTED
        instance.save()
        participiants = ProjectParticipants.objects.create(
            project=instance.project, volunteer=instance.volunteer
        )
        instance.project.participants.add(participiants)   # добавила
        incomes_approve_send_email.delay(
            participiants.pk, get_site_data(self.context.get('request', {}))
        )
        return {
            'message': 'Заявка волонтера принята и добавлена в '
            'участники проекта.'
        }

    def reject_incomes(self, instance):
        """
        Отклоняет заявку волонтера.
        """
        if instance.status_incomes == ProjectIncomes.REJECTED:
            raise serializers.ValidationError('Вы уже отклоняли данную заявку')
        elif instance.status_incomes == ProjectIncomes.ACCEPTED:
            existing_participant = ProjectParticipants.objects.get(
                project=instance.project, volunteer=instance.volunteer
            )
            incomes_reject_send_email.delay(
                existing_participant.pk,
                get_site_data(self.context.get('request', {}))
            )
            existing_participant.delete()
        instance.status_incomes = ProjectIncomes.REJECTED
        instance.save()
        return {'message': 'Заявка волонтера отклонена организатором.'}

    def to_representation(self, instance):
        return ProjectIncomesGetSerializer(instance).data


class OrganizationGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения организации-организатора.
    """

    contact_person = UserSerializer()

    class Meta:
        model = Organization
        fields = '__all__'


class OgranizationCreateSerializer(
    IsValidModifyErrorForFrontendMixin, serializers.ModelSerializer
):
    """
    Сериализатор для создания организации-организатора.
    """

    contact_person = UserCreateSerializer()
    photo = Base64ImageField(required=False)

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('contact_person')

        user_data['role'] = User.ORGANIZER

        user = create_user(self, UserCreateSerializer, user_data)
        organization = Organization.objects.create(
            contact_person=user, **validated_data
        )

        return organization

    class Meta:
        model = Organization
        fields = '__all__'


class OgranizationUpdateSerializer(OgranizationCreateSerializer):
    """
    Сериализатор для редактирования организации-организатора.
    """

    contact_person = UserSerializer()

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('contact_person')
        instance.contact_person.first_name = user_data.get('first_name')
        instance.contact_person.second_name = user_data.get('second_name')
        instance.contact_person.last_name = user_data.get('last_name')
        instance.contact_person.save()

        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()
        return instance


class ProjectFavoriteSerializer(IsValidModifyErrorForFrontendMixin,
                                serializers.ModelSerializer):
    """
    Сериализатор для отображения избранных проектов.
    """

    class Meta:
        model = ProjectFavorite
        fields = (
            'user',
            'project',
        )
        validators = [
            UniqueTogetherValidator(
                ProjectFavorite.objects.all(),
                fields=('user', 'project'),
                message='Этот проект уже присутствует в избранном!',
            )
        ]


class CurrentUserSerializer(UserSerializer):
    """
    Сериализатор текущего пользователя, используется по адресу auth/me.
    """

    id_organizer_or_volunteer = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'second_name',
            'last_name',
            'email',
            'role',
            'id_organizer_or_volunteer',
        )

    def get_id_organizer_or_volunteer(self, obj):
        """
        Метод получает список id организаций или волонтера,
        в зависимости от роли пользователя.
        """
        user = self.context['request'].user

        if user.is_organizer:
            organization = user.organization
            return organization.id if organization else None
        elif user.is_volunteer:
            volunteer = user.volunteers
            return volunteer.id if volunteer else None
        else:
            return None
