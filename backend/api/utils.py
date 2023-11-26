from django.http import Http404
from django.shortcuts import get_object_or_404
from djoser.compat import get_user_email
from djoser.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ValidationError

from projects.models import Project


def create_user(self, serializer, data):
    """
    Функция создания объекта пользователя с отправкой ссылки для активации
    аккаунта и подтверждения завершения процедуры подтверждения email-а.
    """

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
    """
    Функция модификации деталей ошибок валидации в отдельные словари:
    errors_valid - ошибки валидации, errors_db - ошибки БД.
    """

    errors_db_codes = ['unique', 'not_exist', 'wrong']
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
                if details.get(key)[i]['code'] in errors_db_codes:
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


def get_modify_validation_errors(class_name, details, errors_db):
    errors_db, errors_valid = modify_errors(details, {})
    errors_db.update(
        {'ValidationErrors': errors_valid},
    )
    return ValidationError(
        {class_name: errors_db},
    )


def get_instance(model, user, project, serializer_name):
    try:
        instance = get_object_or_404(model, user=user, project=project)
    except ValueError as error:
        raise get_modify_validation_errors(
            serializer_name,
            {
                'id': ValidationError(error.args[0]).get_full_details()
            },
            {},
        )
    except Http404 as error:
        raise get_modify_validation_errors(
            serializer_name,
            {
                'not_exist':
                ValidationError(
                    error.args[0], code='not_exist',
                ).get_full_details()
            },
            {},
        )
    except Exception as error:
        raise get_modify_validation_errors(
            serializer_name,
            {
                'error': ValidationError(error.args[0]).get_full_details()
            },
            {},
        )
    return instance
