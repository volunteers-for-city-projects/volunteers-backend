from django.db import transaction
from django.utils import timezone
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from taggit.models import Tag

from content.models import (
    City,
    Feedback,
    News,
    PlatformAbout,
    Skills,
    Valuation,
)
from projects.models import (
    Address,
    Category,
    Organization,
    Project,
    ProjectIncomes,
    ProjectParticipants,
    Volunteer,
    VolunteerSkills,
)
from users.models import User

from .validators import validate_status_incomes


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
        return Project.objects.count()

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
    Сериализатор для просмотра новостей списком
    """

    tags = TagListSerializerField()

    class Meta:
        model = News
        fields = ('picture', 'title', 'tags', 'created_at')


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для формы обратной связи.
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


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для проекта.
    """

    event_address = AddressSerializer()
    # category = ProjectCategorySerializer()
    # city = CitySerializer()

    def validate_dates(self, start, end, application):
        """
        Проверяет корректность дат.
        """
        now = timezone.now()

        if start <= now:
            raise serializers.ValidationError(
                'Дата начала мероприятия должна быть в будущем.'
            )
        if end <= start:
            raise serializers.ValidationError(
                'Дата окончания мероприятия должна быть позже даты начала.'
            )
        if not (application <= start <= end):
            raise serializers.ValidationError(
                'Дата подачи заявки должна быть позже или равна дате начала '
                'мероприятия и позже даты начала и раньше даты окончания.'
            )
        return start, end, application

    def validate_reception_status(
        self, status_project, application_date, start_datetime, end_datetime
    ):
        """
        Проверяет, что статус "Прием откликов окончен" можно устанавливать
        только после указанной даты подачи заявки.
        """
        now = timezone.now()
        if status_project == Project.RECEPTION_OF_RESPONSES_CLOSED:
            if application_date > now:
                raise serializers.ValidationError(
                    'Статус проекта "Прием откликов окончен" можно установить'
                    'только после окончания подачи заявок.'
                )
        if status_project == Project.READY_FOR_FEEDBACK:
            if now < start_datetime or now < application_date:
                raise serializers.ValidationError(
                    'Статус проекта "Готов к откликам" можно установить до '
                    'начала мероприятия и до даты подачи заявки.'
                )
        if status_project == Project.PROJECT_COMPLETED:
            if now < end_datetime:
                raise serializers.ValidationError(
                    'Статус проекта "Проект завершен" можно установить '
                    'только после окончания мероприятия.'
                )

    def validate(self, data):
        start_datetime = data['start_datetime']
        end_datetime = data['end_datetime']
        application_date = data['application_date']
        status_project = data.get('status_project')

        self.validate_dates(start_datetime, end_datetime, application_date)
        self.validate_reception_status(
            status_project, application_date, start_datetime, end_datetime
        )
        return data

    def create(self, validated_data):
        if validated_data.get('status_approve') not in (
            Project.EDITING,
            Project.PENDING,
        ):
            validated_data.pop('status_approve')
        return super().create(validated_data)

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'picture',
            'start_datetime',
            'end_datetime',
            'application_date',
            'event_purpose',
            'event_address',
            'project_tasks',
            'project_events',
            'organizer_provides',
            'organization',
            'city',
            'category',
            'status_project',
            'photo_previous_event',
            'participants',
            'status_approve',
        )


class SkillsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения навыков.
    """

    class Meta:
        model = Skills
        fields = ('id', 'name')


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


class ProjectIncomesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заявок волонтеров.
    """

    class Meta:
        model = ProjectIncomes
        fields = ('id', 'project', 'volunteer', 'status_incomes', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        project = validated_data['project']
        volunteer = validated_data['volunteer']
        status_incomes = validated_data.get(
            'status_incomes', ProjectIncomes.APPLICATION_SUBMITTED
        )
        existing_application = ProjectIncomes.objects.filter(
            project=project, volunteer=volunteer
        ).first()
        if existing_application:
            existing_application.status_incomes = status_incomes
            existing_application.save()
            return existing_application
        else:
            project_income = ProjectIncomes.objects.create(
                project=project,
                volunteer=volunteer,
                status_incomes=status_incomes,
            )
            return project_income

    def delete(self, instance):
        """
        Удаляет заявку волонтера только если статус APPLICATION_SUBMITTED.
        """
        if instance.status_incomes == ProjectIncomes.APPLICATION_SUBMITTED:
            instance.delete()
        else:
            raise serializers.ValidationError(
                'Невозможно удалить заявку, если статус не "Заявка подана".'
            )

    def validate_status_incomes(self, value):
        return validate_status_incomes(value)

    def accept_incomes(self, instance):
        """
        Принимает заявку волонтера и добавляет его в участники проекта.
        """
        instance.status_incomes = ProjectIncomes.ACCEPTED
        instance.save()
        ProjectParticipants.objects.create(
            project=instance.project, volunteer=instance.volunteer
        )
        return {'message': 'Заявка волонтера принята.'}

    def reject_incomes(self, instance):
        """
        Отклоняет заявку волонтера.
        """
        instance.status_incomes = ProjectIncomes.REJECTED
        instance.save()
        return {'message': 'Заявка волонтера отклонена.'}


class VolunteerGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения волонтера.
    """

    user = UserSerializer(read_only=True)
    skills = SkillsSerializer(many=True)

    class Meta:
        model = Volunteer
        fields = '__all__'


class VolunteerCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания волонтера.
    """

    user = UserCreateSerializer()
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skills.objects.all(), many=True
    )

    def create_skills(self, skills, volunteer):
        data = []
        for skill in skills:
            data.append(VolunteerSkills(volunteer=volunteer, skill=skill))
        VolunteerSkills.objects.bulk_create(data)

    @transaction.atomic
    def create(self, validated_data):
        skills = validated_data.pop('skills')
        user_data = validated_data.pop('user')
        # Убираем из параметров роль, если она указана в JSON явно
        if user_data.get('role') is not None:
            user_data.pop('role')

        user = User.objects.create_user(role=User.VOLUNTEER, **user_data)
        volunteer = Volunteer.objects.create(user=user, **validated_data)
        self.create_skills(skills, volunteer)

        return volunteer

    class Meta:
        model = Volunteer
        exclude = ('id',)


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


class OrganizationGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения организации-организатора.
    """

    contact_person = UserSerializer()

    class Meta:
        model = Organization
        fields = '__all__'


class OgranizationCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания организации-организатора.
    """

    contact_person = UserCreateSerializer()

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('contact_person')
        # Убираем из параметров роль, если она указана в JSON явно
        if user_data.get('role') is not None:
            user_data.pop('role')

        user = User.objects.create_user(role=User.ORGANIZER, **user_data)
        organization = Organization.objects.create(
            contact_person=user, **validated_data
        )

        return organization

    class Meta:
        model = Organization
        exclude = ('id',)


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


class ProjectParticipantSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка участников.
    """

    class Meta:
        model = ProjectParticipants
        fields = (
            'project',
            'volunteer',
        )


class VolunteerProfileSerializer(serializers.Serializer):
    """
    Сериализатор для личного кабинета волонтера.
    """

    user = VolunteerGetSerializer(read_only=True, source='*')
    projects = serializers.SerializerMethodField()
    project_incomes = ProjectIncomesSerializer(many=True, read_only=True)

    def get_projects(self, obj):
        project_participants = ProjectParticipants.objects.filter(
            volunteer__id=obj.id
        )
        projects = [
            participant.project for participant in project_participants
        ]
        project_serializer = ProjectSerializer(projects, many=True)
        return project_serializer.data


class VolunteerFavoriteGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения избранных проектов волонтера.
    """

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'picture',
            'organization',
            'status_project',
        )
