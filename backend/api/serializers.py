from django.utils import timezone
from rest_framework import serializers

from content.models import Feedback, News, PlatformAbout, Valuation
from projects.models import Project


class ValuationSerializer(serializers.ModelSerializer):
    '''Сериализатор для отображения ценностей платформы.'''

    class Meta:
        model = Valuation
        fields = ('title', 'description')


class PlatformAboutSerializer(serializers.ModelSerializer):
    '''Сериалзиатор для отображения информации о платформе.'''

    valuations = ValuationSerializer(many=True)

    class Meta:
        model = PlatformAbout
        fields = ('about_us', 'platform_email', 'valuations')


class TagListSerializerField(serializers.Serializer):
    '''Возвращает список хештегов для новостей.'''

    def to_representation(self, value):
        return [tag.name for tag in value.all()]


class NewsSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра новости в детализации.'''

    tags = TagListSerializerField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('picture', 'tags', 'title', 'text', 'author', 'created_at')

    def get_author(self, obj):
        return f'{obj.author.first_name} {obj.author.last_name}'


class PreviewNewsSerializer(serializers.ModelSerializer):
    '''Сериализатор для просмотра новостей списком.'''

    tags = TagListSerializerField()

    class Meta:
        model = News
        fields = ('picture', 'title', 'tags', 'created_at')


class FeedbackSerializer(serializers.ModelSerializer):
    '''Сериализатор для формы обратной связи.'''

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'text')


class ProjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Project.
    """

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
                'Дата подачи заявки должна быть в будущем, '
                'позже даты начала и раньше даты окончания.'
            )
        return start, end, application

    def validate_reception_status(self, status_project, application_date):
        """
        Проверяет, что статус "Прием откликов окончен" можно устанавливать
        только после указанной даты подачи заявки.
        """
        now = timezone.now()

        if (
            status_project == Project.RECEPTION_OF_RESPONSES_CLOSED
            and application_date > now
        ):
            raise serializers.ValidationError(
                'Статус "Прием откликов окончен" можно установить'
                'только после окончания подачи заявок.'
            )

    def validate(self, data):
        start_datatime = data['start_datatime']
        end_datatime = data['end_datatime']
        application_date = data['application_date']
        status_project = data.get('status_project')

        self.validate_dates(start_datatime, end_datatime, application_date)
        self.validate_reception_status(status_project, application_date)

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
