from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from projects.models import Organization, Volunteer


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
    def is_valid(self, *, raise_exception=False):
        try:
            super().is_valid(raise_exception=True)
        except ValidationError as error:
            keys = error.detail.keys()
            modified_errors = {}
            for key in keys:
                if isinstance(error.detail.get(key), dict):
                    modified_errors.update(error.detail.get(key))
                else:
                    modified_errors[key] = error.detail.get(key)
            raise ValidationError(
                {
                    self.__class__.__name__: modified_errors
                }
            )
        return bool(self._errors)
