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


def validate_dates(start, end, application):
    """
    Проверяет корректность дат.
    """
    now = timezone.now()

    if start <= now:
        raise serializers.ValidationError(
            'Дата начала мероприятия должна быть в будущем.'
        )
    if end <= start:
        raise serializers.ValidationError(
            'Дата окончания мероприятия должна быть позже даты начала.'
        )
    if not (application <= start <= end):
        raise serializers.ValidationError(
            'Дата подачи заявки должна быть позже или равна дате начала '
            'мероприятия и позже даты начала и раньше даты окончания.'
        )
    return start, end, application


def validate_reception_status(
    self, status_project, application_date, start_datetime, end_datetime
):
    """
    Проверяет, что статус "Прием откликов окончен" можно устанавливать
    только после указанной даты подачи заявки.
    """
    now = timezone.now()
    if status_project == Project.RECEPTION_OF_RESPONSES_CLOSED:
        if application_date > now:
            raise serializers.ValidationError(
                'Статус проекта "Прием откликов окончен" можно установить'
                'только после окончания подачи заявок.'
            )
    if status_project == Project.READY_FOR_FEEDBACK:
        if now < start_datetime or now < application_date:
            raise serializers.ValidationError(
                'Статус проекта "Готов к откликам" можно установить до '
                'начала мероприятия и до даты подачи заявки.'
            )
    if status_project == Project.PROJECT_COMPLETED:
        if now < end_datetime:
            raise serializers.ValidationError(
                'Статус проекта "Проект завершен" можно установить '
                'только после окончания мероприятия.'
            )
