from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOrganizerPermission(BasePermission):
    """Разрешает доступ только пользователям с ролью организатор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_organizer

    def has_object_permission(self, request, view, project):
        return (
            request.user.is_authenticated and project.organizer == request.user
        )


class IsVolunteerPermission(BasePermission):
    """Разрешает доступ только пользователям с ролью волонтер."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_volunteer
