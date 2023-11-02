from django.utils import timezone
from rest_framework import serializers

from projects.models import Project, ProjectIncomes


def validate_status_incomes(value):
    """
    Проверяет, что статус заявки является допустимым.
    """
    if value not in dict(ProjectIncomes.STATUS_INCOMES).keys():
        raise serializers.ValidationError('Недопустимый статус заявки.')
    return value


def validate_dates(event_start_date, event_end_date, application_date):
    """
    Проверяет корректность дат для мероприятия.

    param event_start_date: Дата начала мероприятия.
    param event_end_date: Дата окончания мероприятия.
    param application_date: Дата подачи заявки.
    raises: serializers.ValidationError, если даты не соответствуют условиям.
    """
    now = timezone.now()
    validation_rules = [
        (
            event_start_date <= now,
            'Дата начала мероприятия должна быть в будущем.',
        ),
        (
            event_end_date <= event_start_date,
            'Дата окончания мероприятия должна быть позже даты начала.',
        ),
        (
            not (application_date <= event_start_date <= event_end_date),
            'Дата подачи заявки должна быть позже или равна дате начала '
            'мероприятия и позже даты начала и раньше даты окончания.',
        ),
    ]

    for condition, error_message in validation_rules:
        if condition:
            raise serializers.ValidationError(error_message)
    return event_start_date, event_end_date, application_date


# нужно передалть с учетом, изменений реализации статусов.
def validate_reception_status(
    status_project, application_date, start_datetime, end_datetime
):
    """
    Проверяет, что статус можно устанавливать
    только после указанной даты.
    """
    now = timezone.now()
    validation_rules = [
        (
            Project.RECEPTION_OF_RESPONSES_CLOSED,
            application_date > now,
            'Статус проекта "Прием откликов окончен" можно установить только '
            'после окончания подачи заявок.',
        ),
        (
            Project.READY_FOR_FEEDBACK,
            now < start_datetime or now < application_date,
            'Статус проекта "Готов к откликам" можно установить до начала '
            'мероприятия и до даты подачи заявки.',
        ),
        (
            Project.PROJECT_COMPLETED,
            now < end_datetime,
            'Статус проекта "Проект завершен" можно установить только '
            'после окончания мероприятия.',
        ),
    ]

    for project_status, condition, error_message in validation_rules:
        if status_project == project_status and condition:
            raise serializers.ValidationError(error_message)
