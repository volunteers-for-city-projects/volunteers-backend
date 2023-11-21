from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from projects.models import Organization, Volunteer

from .utils import modify_errors


class DestroyUserMixin:
    """
    Удаление экземляра модели со взаимосвязанной сущностью пользователя.
    Предварительно удаляется добавленное изображение.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        storage = instance.photo.storage
        name = instance.photo.name
        self.perform_destroy(instance)
        try:
            with transaction.atomic():
                if isinstance(instance, Organization):
                    instance.contact_person.delete()
                elif isinstance(instance, Volunteer):
                    instance.user.delete()
        finally:
            if (name and storage.exists(name)):
                storage.delete(name)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsValidModifyErrorForFrontendMixin:
    """
    Миксин для перехвата ошибок валидации и модификации их деталей.
    Переопределен метод проверки данных на валидность. Детали перехваченных
    ошибок анализируются, и формируется словарь деталей ошибок со структурой
    более удобной для фронтов.
    """

    def is_valid(self, *, raise_exception=False):
        try:
            super().is_valid(raise_exception=True)
        except ValidationError as error:
            errors_db, errors_valid = modify_errors(
                error.get_full_details(), {}
            )
            errors_db.update({'ValidationErrors': errors_valid})
            raise ValidationError(
                {
                    self.__class__.__name__:
                    errors_db
                }
            )
        return not bool(self._errors)
