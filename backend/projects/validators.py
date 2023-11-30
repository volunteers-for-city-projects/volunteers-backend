import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.utils.deconstruct import deconstructible

ERROR_MESSAGE_REGEX = 'Недопустимые символы. Разрешены латинские '
'и кириллические буквы, цифры и спецсимволы.',
REGEX_PATTERN = r'^[A-Za-zА-Яа-я0-9 !"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~]+$'


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
        regex=r'^@[A-Za-z\d_]+$',
        # regex=r'^@[\w]+$',
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
    Валидирует длину и символы в Названии организации.
    """
    regex_validator = RegexValidator(
        regex=r'^[а-яА-ЯёЁ\d\s\-\.\,\&\+\№\!\«\»]+$',
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


def validate_name(value):
    """
    Валидация названия проекта.
    """
    MIN_LEN = settings.MIN_LEN_NAME_PROJECT
    MAX_LEN = settings.MAX_LEN_NAME_PROJECT
    NAME_REGEX = r'^[A-Za-zА-Яа-я0-9 !"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~]+$'

    min_length_validator = MinLengthValidator(
        MIN_LEN,
        message=f'Минимальная длина поля должна быть: {MIN_LEN}.',
    )
    max_length_validator = MaxLengthValidator(
        MAX_LEN,
        message=f'Максимальная длина поля должна быть: {MAX_LEN}.',
    )
    regex_validator = RegexValidator(
        regex=NAME_REGEX,
        message='Недопустимые символы в названии проекта. Разрешены латинские '
        'и кириллические буквы, цифры и спецсимволы.',
    )
    min_length_validator(value)
    max_length_validator(value)
    regex_validator(value)


def validate_description(value):
    """
    Валидация описания проекта.
    """
    MIN_LEN = 2
    MAX_LEN = 750

    min_length_validator = MinLengthValidator(
        MIN_LEN,
        message='Минимальная длина поля должна быть: {MIN_LEN} ',
    )
    max_length_validator = MaxLengthValidator(
        MAX_LEN,
        message='Максимальное длина поля должна быть: {MAX_LEN} ',
    )
    min_length_validator(value)
    max_length_validator(value)


def regex_string_validator(value):
    """
    Проверяет, соответствует ли данное значение шаблону, который допускает
    латинские и кириллические буквы, цифры и большинство специальных символов.
    Аргументы: value (str): Строка для валидации.
    Возвращает:
    bool: True, если строка соответствует шаблону, иначе False.
    """

    try:
        RegexValidator(
            regex=REGEX_PATTERN, message=ERROR_MESSAGE_REGEX, code='invalid'
        )(value)
    except ValidationError:
        raise
    return True


@deconstructible
class LengthValidator:
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(
                f'Длина строки должна быть не менее '
                f'{self.min_length} символов.'
            )
        if len(value) > self.max_length:
            raise ValidationError(
                f'Длина строки не должна превышать {self.max_length} символов.'
            )


def validate_text_field(value):
    """
    Валидирует длину и символы в информации об организации.
    """
    regex_validator = RegexValidator(
        regex=r'^[A-Za-zА-Яа-я0-9 №«»\\!"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~]+$',
        # regex=r"(^[%!#$&*'+/=?^_;():@,.<>`{|}~-«»0-9A-ZА-ЯЁ\s]+)\Z",
        message=settings.MESSAGE_ABOUT_US_REGEX_VALID,
        flags=re.I,
    )
    min_length_validator = MinLengthValidator(
        settings.MIN_LEN_ABOUT_US,
        message=settings.MESSAGE_ABOUT_US_VALID,
    )
    max_length_validator = MaxLengthValidator(
        settings.MAX_LEN_ABOUT_US,
        message=settings.MESSAGE_ABOUT_US_VALID,
    )

    min_length_validator(value)
    max_length_validator(value)
    regex_validator(value)


def validate_text_cover_letter(value):
    """
    Валидирует длину и символы в информации об организации.
    """
    regex_validator = RegexValidator(
        regex=r'^[A-Za-zА-Яа-я0-9 №«»\\!"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~]+$',
        # regex=r"(^[%!#$&*'+/=?^_;():@,.<>`{|}~-«»0-9A-ZА-ЯЁ\s]+)\Z",
        message=settings.MESSAGE_ABOUT_US_REGEX_VALID,
        flags=re.I,
    )
    min_length_validator = MinLengthValidator(
        settings.MIN_LEN_COVER_LETTER,
        message=settings.MESSAGE_COVER_LETTER_VALID,
    )
    max_length_validator = MaxLengthValidator(
        settings.MAX_LEN_COVER_LETTER,
        message=settings.MESSAGE_COVER_LETTER_VALID,
    )

    min_length_validator(value)
    max_length_validator(value)
    regex_validator(value)
