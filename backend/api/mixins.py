from rest_framework import status
from rest_framework.response import Response

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
