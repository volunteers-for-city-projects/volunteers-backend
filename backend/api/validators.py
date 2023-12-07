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
    start_datetime,
    end_datetime,
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
    NOW = timezone.now()
    MAX_ALLOWED_DATE = NOW + timezone.timedelta(days=365)
    # MIN_DURATION = timezone.timedelta(minutes=10)
    MAX_DURATION = timezone.timedelta(days=21)
    MIN_DURATION_APPLICATION = timezone.timedelta(days=7)
    MIN_TIME = 8
    MAX_TIME = 22
    MIN_DURATION_TIME = timezone.timedelta(hours=2)
    MAX_DURATION_TIME = timezone.timedelta(hours=9)
    errors = {}

    if not (NOW <= start_date_application <= MAX_ALLOWED_DATE):
        errors.setdefault('start_date_application', []).append(
            'Заявку можно подать в течение года, начиная от текущей даты'
        )
    if not (
        start_date_application + MIN_DURATION_APPLICATION
        <= end_date_application <= start_date_application + MAX_DURATION
        <= MAX_ALLOWED_DATE
    ):
        errors.setdefault('end_date_application', []).append(
            'Окончание приема заявок должно быть не ранее чем через 7 дней и '
            'не позднее чем за 21 день после начала подачи заявок, '
            'а также не позже года от текущей даты.'
        )
    if not (end_date_application <= start_datetime <= MAX_ALLOWED_DATE):
        errors.setdefault('start_datetime', []).append(
            'Дата начала мероприятия должна быть поздее даты окончания '
            'приема заявок и не позднее года от текущей даты'
        )
    if (
        start_datetime.time().hour < MIN_TIME
        or start_datetime.time().hour > (MAX_TIME - 2)
    ):
        errors.setdefault('start_datetime', []).append(
            'Время начала мероприятия должно быть между 8:00 и 20:00.'
        )

    if (
        end_datetime.time().hour < (MIN_TIME + 2)
        or end_datetime.time().hour > MAX_TIME
    ):
        errors.setdefault('end_datetime', []).append(
            'Время окончания мероприятия должно быть между 10:00 и 22:00.'
        )

    if not (
        start_datetime + MIN_DURATION_TIME
        <= end_datetime <= start_datetime + MAX_DURATION <= MAX_ALLOWED_DATE
    ):
        errors.setdefault('end_datetime', []).append(
            'Дата окончания мероприятия должна быть не ранее чем через 2 часа '
            'и не позднее чем за 21 день от даты начала мероприятия, а также '
            'не позже года от текущей даты'
        )

    if not (
        MIN_DURATION_TIME.seconds
        <= (end_datetime - start_datetime).seconds
        <= MAX_DURATION_TIME.seconds
    ):
        errors.setdefault('end_datetime', []).append(
            'Длительность мероприятия должна быть не менее '
            '2 часов и не более 9 часов.'
        )

    if errors:
        raise serializers.ValidationError(errors)

    return (
        start_datetime,
        end_datetime,
        start_date_application,
        end_date_application,
    )
