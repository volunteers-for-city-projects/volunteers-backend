from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from projects.models import Organization, Volunteer

from .utils import get_modify_validation_errors


class DestroyUserMixin:
    """
    Удаление экземляра модели со взаимосвязанной сущностью пользователя.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            self.perform_destroy(instance)
            if isinstance(instance, Organization):
                instance.contact_person.delete()
            elif isinstance(instance, Volunteer):
                instance.user.delete()
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
            raise get_modify_validation_errors(
                self.__class__.__name__,
                error.get_full_details(),
                {},
            )
        return not bool(self._errors)
