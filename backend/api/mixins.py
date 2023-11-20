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
        self.perform_destroy(instance)
        if isinstance(instance, Organization):
            instance.contact_person.delete()
        elif isinstance(instance, Volunteer):
            instance.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        if (
            instance.photo.name
            and instance.photo.storage.exists(instance.photo.name)
        ):
            instance.photo.storage.delete(instance.photo.name)
        instance.delete()


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
