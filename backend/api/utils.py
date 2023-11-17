from djoser.compat import get_user_email
from djoser.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ValidationError

from projects.models import Project


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


def is_correct_status_change(status_before, status_new):
    """
    Метод проверяет может ли текущий статус проекта
    переходить в новый(запрашиваемый) статус
    """

    allowed_status_changes = {
        Project.EDITING: (Project.EDITING, Project.PENDING),
        Project.PENDING: (Project.APPROVED, Project.REJECTED),
        Project.REJECTED: (Project.EDITING, Project.PENDING),
        Project.APPROVED: (Project.APPROVED, Project.CANCELED_BY_ORGANIZER),
        # Project.CANCELED_BY_ORGANIZER: [Project.EDITING],  # Может изменится
    }
    return status_new in allowed_status_changes.get(status_before, ())


class NonEmptyBase64ImageField(Base64ImageField):

    def to_internal_value(self, data):
        """
        Преобразует в класс, не позволяющий отправлять пустую строку
        в изображении.
        """

        value = super().to_internal_value(data)
        if value in [None, ""]:
            raise ValidationError("Поле c изображением не может быть пустым.")
        return value


def modify_errors(details, errors_valid):
    keys = details.keys()
    errors_db = {}
    for key in keys:
        if isinstance(details.get(key), dict):
            inner_details, inner_valid = modify_errors(
                details.get(key), errors_valid)
            for key_in in inner_details.keys():
                errors_db.setdefault(
                    key_in,
                    []
                ).append(inner_details.get(key_in)[0])
        else:
            for i in range(len(details.get(key))):
                if details.get(key)[i]['code'] in ['unique', 'not_exist']:
                    errors_db.setdefault(
                        key,
                        []
                    ).append(str(details.get(key)[i].get('message')))
                else:
                    errors_valid.setdefault(
                        key,
                        []
                    ).append(str(details.get(key)[i].get('message')))
    return errors_db, errors_valid
