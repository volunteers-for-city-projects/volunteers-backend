from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOrganizerPermission(BasePermission):
    """Разрешает доступ только пользователям с ролью организатор."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.role == User.ORGANIZER
        )


class IsVolunteerPermission(BasePermission):
    """Разрешает доступ только пользователям с ролью волонтер."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_volunteer
