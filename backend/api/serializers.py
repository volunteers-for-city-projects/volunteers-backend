from rest_framework import serializers

from content.models import News, Valuation, PlatformAbout, Feedback


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
