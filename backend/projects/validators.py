from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from backend.settings import (
    LEN_PHONE,
    MAX_LEN_TELEGRAM,
    MESSAGE_PHONE_REGEX,
    MIN_LEN_TELEGRAM,
    OGRN_ERROR_MESSAGE,
    TELEGRAM_ERROR_MESSAGE,
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
        regex=r'^\d{13}$', message=OGRN_ERROR_MESSAGE
    )
    ogrn_max_length = MaxLengthValidator(13, message=OGRN_ERROR_MESSAGE)
    ogrn_min_length = MinLengthValidator(13, message=OGRN_ERROR_MESSAGE)

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
        regex=r'^\+7\d{10}$', message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )
    phone_max_length = MaxLengthValidator(
        LEN_PHONE, message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )
    phone_min_length = MinLengthValidator(
        LEN_PHONE, message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )

    regex_validator(value)
    phone_max_length(value)
    phone_min_length(value)


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
        message=TELEGRAM_ERROR_MESSAGE.format(
            MIN_LEN_TELEGRAM, MAX_LEN_TELEGRAM
        ),
    )
    min_length_validator = MinLengthValidator(
        MIN_LEN_TELEGRAM,
        message=TELEGRAM_ERROR_MESSAGE.format(
            MIN_LEN_TELEGRAM, MAX_LEN_TELEGRAM
        ),
    )
    max_length_validator = MaxLengthValidator(
        MAX_LEN_TELEGRAM,
        message=TELEGRAM_ERROR_MESSAGE.format(
            MIN_LEN_TELEGRAM, MAX_LEN_TELEGRAM
        ),
    )

    regex_validator(value)
    min_length_validator(value)
    max_length_validator(value)