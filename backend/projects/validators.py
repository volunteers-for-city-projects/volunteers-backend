import re

from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)


def validate_ogrn(value):
    """
    Валидирует ОГРН.
    Параметры:
    value (str): Значение ОГРН для валидации.
    Исключения:
    ValidationError: Если ОГРН не соответствует формату (13 цифр).
    Возвращает:
    None
    """
    regex_validator = RegexValidator(
        regex=r'^\d{13}$', message=settings.OGRN_ERROR_MESSAGE
    )
    ogrn_max_length = MaxLengthValidator(
        settings.LEN_OGRN, message=settings.OGRN_ERROR_MESSAGE
    )
    ogrn_min_length = MinLengthValidator(
        settings.LEN_OGRN, message=settings.OGRN_ERROR_MESSAGE
    )

    regex_validator(value)
    ogrn_max_length(value)
    ogrn_min_length(value)


def validate_phone_number(value):
    """
    Валидирует номер телефона.
    Параметры:
    value (str): Значение номера телефона для валидации.
    Исключения:
    ValidationError: Если номер телефона не соответствует формату
                    (+7 и 10 цифр).
    Возвращает:
    None
    """
    regex_validator = RegexValidator(
        regex=r'^\+7\d{10}$',
        message=settings.MESSAGE_PHONE_REGEX,
    )
    # phone_max_length = MaxLengthValidator(
    #     settings.LEN_PHONE,
    #     message=settings.MESSAGE_PHONE_REGEX,
    # )
    # phone_min_length = MinLengthValidator(
    #     settings.LEN_PHONE,
    #     message=settings.MESSAGE_PHONE_REGEX,
    # )

    regex_validator(value)
    # phone_max_length(value)
    # phone_min_length(value)


def validate_telegram(value):
    """
    Валидирует Telegram никнейм.
    Параметры:
    value (str): Значение Telegram никнейма для валидации.
    Исключения:
    ValidationError: Если Telegram никнейм не соответствует формату
                    (@ и буквы, цифры, знаки подчеркивания),
                    или если он не соответствует минимальной
                    или максимальной длине.
    Возвращает:
    None
    """
    regex_validator = RegexValidator(
        regex=r'^@[\w]+$',
        message=settings.TELEGRAM_ERROR_MESSAGE,
    )
    min_length_validator = MinLengthValidator(
        settings.MIN_LEN_TELEGRAM,
        message=settings.TELEGRAM_ERROR_MESSAGE,
    )
    max_length_validator = MaxLengthValidator(
        settings.MAX_LEN_TELEGRAM,
        message=settings.TELEGRAM_ERROR_MESSAGE,
    )

    regex_validator(value)
    min_length_validator(value)
    max_length_validator(value)


def validate_title(value):
    """
    Валидирует длину и символы в Названии проекта.
    """
    regex_validator = RegexValidator(
        regex=r'^[а-яА-ЯёЁ\d\s\-\.\,\&\+\№\!]+$',
        message=settings.MESSAGE_TITLE_CYRILLIC,
    )
    min_length_validator = MinLengthValidator(
        settings.MIN_LEN_TITLE,
        message=settings.MESSAGE_TITLE_VALID,
    )
    max_length_validator = MaxLengthValidator(
        settings.MAX_LEN_TITLE,
        message=settings.MESSAGE_TITLE_VALID,
    )

    regex_validator(value)
    min_length_validator(value)
    max_length_validator(value)


def validate_about(value):
    """
    Валидирует длину и символы в информации об организации.
    """
    regex_validator = RegexValidator(
        regex=r"(^[-!#$%&'*+/=?^_;():@,.<>`{}|~0-9A-ZА-ЯЁ\s]+)\Z",
        message=settings.MESSAGE_ABOUT_US_REGEX_VALID,
        flags=re.I
    )
    min_length_validator = MinLengthValidator(
        settings.MIN_LEN_ABOUT_US,
        message=settings.MESSAGE_ABOUT_US_VALID,
    )
    max_length_validator = MaxLengthValidator(
        settings.MAX_LEN_ABOUT_US,
        message=settings.MESSAGE_ABOUT_US_VALID,
    )

    regex_validator(value)
    min_length_validator(value)
    max_length_validator(value)
    regex_validator(value)
