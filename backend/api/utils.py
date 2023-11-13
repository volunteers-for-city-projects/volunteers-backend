from djoser.compat import get_user_email
from djoser.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ValidationError


def create_user(self, serializer, data):
    user_serializer = serializer(data=data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(
                self.context.get('request'), context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(
                self.context.get('request'), context).send(to)
    return user


class NonEmptyBase64ImageField(Base64ImageField):

    def to_internal_value(self, data):
        """
        Преобразует в класс, не позволяющий отправлять пустую строку.
        """

        value = super().to_internal_value(data)
        if value in [None, ""]:
            raise ValidationError("Поле c изображением не может быть пустым.")
        return value
