from rest_framework import serializers
from projects.models import ProjectIncomes


def validate_status_incomes(value):
    """
    Проверяет, что статус заявки является допустимым.
    """
    if value not in dict(ProjectIncomes.STATUS_INCOMES).keys():
        raise serializers.ValidationError('Недопустимый статус заявки.')
    return value
