from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from backend.settings import (
    MAX_LENGTH_EMAIL_USER_PART,
    MESSAGE_EMAIL_NOT_VALID,
    MESSAGE_EMAIL_USER_PART_VALID,
)


class EmailValidator:
    """
    Проверка длинны пользовательской части email адреса.
    """

    email_max_length = MaxLengthValidator(
        MAX_LENGTH_EMAIL_USER_PART,
        message=MESSAGE_EMAIL_USER_PART_VALID
    )

    @classmethod
    def validate_email(cls, value):
        try:
            user_part, domain_part = value.rsplit("@", 1)
        except ValueError:
            raise ValidationError(MESSAGE_EMAIL_NOT_VALID)
        cls.email_max_length(user_part)
