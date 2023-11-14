from django.utils import timezone
from rest_framework import serializers

from projects.models import ProjectIncomes


def validate_status_incomes(value):
    """
    Проверяет, что статус заявки является допустимым.
    """
    if value not in dict(ProjectIncomes.STATUS_INCOMES).keys():
        raise serializers.ValidationError('Недопустимый статус заявки.')
    return value


def validate_dates(
    start_date,
    end_date,
    start_date_application,
    end_date_application,
):
    """
    Проверяет корректность дат для мероприятия.

    param event_start_date: Дата начала мероприятия.
    param event_end_date: Дата окончания мероприятия.
    param start_date_application: Дата начало подачи заявки.
    param end_date_application: Дата окончания подачи заявки.
    raises: serializers.ValidationError, если даты не соответствуют условиям.
    """
    now = timezone.now()
    max_allowed_date = now + timezone.timedelta(days=365)

    if (
        start_date_application <= now
        and start_date_application < max_allowed_date
    ):
        raise serializers.ValidationError(
            'Начало подачи заявки должна быть текущим или будущем и '
            'не более чем через год после текущей даты.'
        )
    if (
        end_date_application
        <= start_date_application + timezone.timedelta(minutes=10)
        and end_date_application < max_allowed_date
    ):
        raise serializers.ValidationError(
            'Окончания подачи заявки должна быть позже начала и '
            'не более чем через год после текущей даты.'
        )
    if (
        start_date <= end_date_application
        and start_date < max_allowed_date
    ):
        raise serializers.ValidationError(
            'Начало мероприятия должна быть в будущем после окончания '
            'подачи заявок и не более чем через год после текущей даты.'
        )
    if (
        end_date <= start_date + timezone.timedelta(minutes=10)
        and end_date < max_allowed_date
    ):
        raise serializers.ValidationError(
            'Дата окончания мероприятия должна быть позже начала и '
            'не более чем через год после текущей даты.'
        )
    return (
        start_date,
        end_date,
        start_date_application,
        end_date_application,
    )


# TODO нужно передалть с учетом, изменений реализации статусов.
# def validate_reception_status(
#     status_project, application_date, start_datetime, end_datetime
# ):
#     """
#     Проверяет, что статус можно устанавливать
#     только после указанной даты.
#     """
#     now = timezone.now()
#     validation_rules = [
#         (
#             Project.RECEPTION_OF_RESPONSES_CLOSED,
#             application_date > now,
#             'Статус проекта "Прием откликов окончен" можно установить '
#             'только после окончания подачи заявок.',
#         ),
#         (
#             Project.READY_FOR_FEEDBACK,
#             now < start_datetime or now < application_date,
#             'Статус проекта "Готов к откликам" можно установить до начала '
#             'мероприятия и до даты подачи заявки.',
#         ),
#         (
#             Project.PROJECT_COMPLETED,
#             now < end_datetime,
#             'Статус проекта "Проект завершен" можно установить только '
#             'после окончания мероприятия.',
#         ),
#     ]

#     for project_status, condition, error_message in validation_rules:
#         if status_project == project_status and condition:
#             raise serializers.ValidationError(error_message)
