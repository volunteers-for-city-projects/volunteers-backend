from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from backend.settings import (
    MAX_LEN_NAME_USER,
    MESSAGE_NAME_USER_CYRILLIC,
    MESSAGE_NAME_USER_VALID,
    MIN_LEN_NAME_USER,
)


class NameUserValidator:
    """
    Проверка на ввод текста кириллицей.
    """

    name_regex = RegexValidator(
        regex=r'^[а-яА-ЯёЁ\-]+$',
        message=MESSAGE_NAME_USER_CYRILLIC
    )
    name_max_length = MaxLengthValidator(
        MAX_LEN_NAME_USER,
        message=MESSAGE_NAME_USER_VALID
    )
    name_min_length = MinLengthValidator(
        MIN_LEN_NAME_USER,
        message=MESSAGE_NAME_USER_VALID
    )

    @classmethod
    def validate_name(cls, value):
        cls.name_regex(value)
        cls.name_max_length(value)
        cls.name_min_length(value)
