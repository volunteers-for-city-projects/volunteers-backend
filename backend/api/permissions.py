from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsOrganizer(BasePermission):
    """Разрешает доступ только пользователям с ролью организатор."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.role == User.ORGANIZER
        )


class IsOrganizerOfProject(BasePermission):
    """
    Разрешает доступ только организатору проекта.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_organizer
            and obj.project.organization.contact_person == request.user
        )


class IsVolunteer(BasePermission):
    """Разрешает доступ только пользователям с ролью волонтер."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.VOLUNTEER
        )


class IsVolunteerOfIncomes(BasePermission):
    """
    Разрешает доступ только волонтеру, который создал заявку. Проверяет,
    что пользователь аутентифицирован и имеет связь с объектом Volunteer,
    который соответствует волонтеру, указанному в заявке.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_volunteer

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_volunteer
            and obj.volunteer == request.user.volunteers
        )


class IsOwnerOrReadOnlyPermission(BasePermission):
    """Разрешает доступ только создателю объекта для изменения/удаления."""

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.volunteer == request.user
