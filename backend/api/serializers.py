from django.db import transaction
from django.shortcuts import get_object_or_404
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
    Category,
    Organization,
    Project,
    ProjectIncomes,
    ProjectParticipants,
    Volunteer,
    VolunteerSkills,
)
from users.models import User


class ValuationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ценностей платформы.
    """

    class Meta:
        model = Valuation
        fields = ('title', 'description')


class PlatformAboutSerializer(serializers.ModelSerializer):
    '''Сериалзиатор для отображения информации о платформе.'''

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
        return User.objects.filter(role='organizer').count()


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
    Сериализатор для Project.
    """

    category = ProjectCategorySerializer()
    city = CitySerializer()

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
        if not (start <= application <= end):
            raise serializers.ValidationError(
                'Дата подачи заявки должна быть позже или равна дате начала '
                'мероприятия и позже даты начала и раньше даты окончания.'
            )
        return start, end, application

    def validate_reception_status(
        self, status_project, application_date, start_datatime, end_datatime
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
            if not (start_datatime <= application_date <= end_datatime):
                raise serializers.ValidationError(
                    'Статус проекта "Готов к откликам" можно установить '
                    'в период с даты начала мероприятия до даты подачи заявки.'
                )
        if status_project == Project.PROJECT_COMPLETED:
            if now < end_datatime:
                raise serializers.ValidationError(
                    'Статус проекта "Проект завершен" можно установить '
                    'только после окончания мероприятия.'
                )

    def validate(self, data):
        start_datatime = data['start_datatime']
        end_datatime = data['end_datatime']
        application_date = data['application_date']
        status_project = data.get('status_project')

        self.validate_dates(start_datatime, end_datatime, application_date)
        self.validate_reception_status(
            status_project, application_date, start_datatime, end_datatime
        )

        return data

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
        fields = '__all__'


class VolunteerGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения волонтера.
    """

    user = UserSerializer()
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

        user = User.objects.create_user(role=User.VOLUNTEER, **user_data)
        volunteer = Volunteer.objects.create(user=user, **validated_data)
        self.create_skills(skills, volunteer)

        return volunteer

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     skills = validated_data.pop('skills')
    #     VolunteerSkills.objects.filter(volunteer=instance).delete()
    #     self.create_skills(skills, instance)

    #     user_data = validated_data.pop('user')
    #     user = User.objects.get(email=user_data.get('email'))
    #     user.first_name = user_data.get('first_name')
    #     user.second_name = user_data.get('second_name')
    #     user.last_name = user_data.get('last_name')
    #     user.save()

    #     for attr, value in validated_data.items():
    #         if hasattr(instance, attr):
    #             setattr(instance, attr, value)

    #     instance.save()
    #     return instance

    class Meta:
        model = Volunteer
        exclude = ('id',)


class VolunteerUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования волонтера.
    """

    user = UserSerializer()
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skills.objects.all(), many=True
    )

    def create_skills(self, skills, volunteer):
        data = []
        for skill in skills:
            data.append(VolunteerSkills(volunteer=volunteer, skill=skill))
        VolunteerSkills.objects.bulk_create(data)

    @transaction.atomic
    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        VolunteerSkills.objects.filter(volunteer=instance).delete()
        self.create_skills(skills, instance)

        user_data = validated_data.pop('user')
        email = user_data.get('email')
        user = get_object_or_404(User, email=email)
        user.first_name = user_data.get('first_name')
        user.second_name = user_data.get('second_name')
        user.last_name = user_data.get('last_name')
        user.save()

        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = Volunteer
        exclude = ('id',)


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
        user = User.objects.create_user(role=User.ORGANIZER, **user_data)
        organization = Organization.objects.create(
            contact_person=user, **validated_data
        )

        return organization

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('contact_person')
        user = User.objects.get(email=user_data.get('email'))
        user.first_name = user_data.get('first_name')
        user.second_name = user_data.get('second_name')
        user.last_name = user_data.get('last_name')
        user.save()

        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = Organization
        exclude = ('id',)


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


# class VolunteerProfileSerializer(serializers.Serializer):
#     """
#     Сериализатор для личного кабинета волонтера.
#     """

#     user = VolunteerGetSerializer(source='*')
#     projects = ProjectSerializer(
#         many=True,
#         read_only=True,
#         source='volunteer.projectparticipants_set.project',
#     )
#     project_incomes = ProjectIncomesSerializer(many=True, read_only=True)

#     class Meta:
#         fields = '__all__'


class VolunteerProfileSerializer(serializers.Serializer):
    """
    Сериализатор для личного кабинета волонтера.
    """

    user = VolunteerGetSerializer(read_only=True, source='*')
    # projects = ProjectParticipantSerializer(
    #     many=True,
    #     read_only=True,
    #     source='volunteer.projectparticipants_set',
    # )
    projects = serializers.SerializerMethodField()
    project_incomes = ProjectIncomesSerializer(many=True, read_only=True)

    class Meta:
        model = Volunteer
        fields = '__all__'

    def get_projects(self, obj):
        # return Project.objects.filter(obj='participants__volunteer')

        projects = Project.objects.filter(
            # participants__volunteer=obj
            # obj=project__projects_volunteers__volunteer
            participants__projects_volunteers__volunteer=obj
        )
        return projects
