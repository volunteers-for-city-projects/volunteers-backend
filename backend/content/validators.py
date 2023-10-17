from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from backend.settings import (
    LEN_PHONE,
    MAX_LEN_NAME_FEEDBACK,
    MAX_LEN_TEXT_FEEDBACK,
    MESSAGE_NAME_FEEDBACK_CYRILLIC,
    MESSAGE_NAME_FEEDBACK_VALID,
    MESSAGE_PHONE_REGEX,
    MESSAGE_TEXT_FEEDBACK_VALID,
    MIN_LEN_NAME_FEEDBACK,
    MIN_LEN_TEXT_FEEDBACK,
)


class PhoneValidator:
    '''Валидация номере телефона на соответствие формата +70000000000.'''

    regex_validator = RegexValidator(
        regex=r'^\+7\d{10}$',
        message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )
    phone_max_length = MaxLengthValidator(
        LEN_PHONE,
        message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )
    phone_min_length = MinLengthValidator(
        LEN_PHONE,
        message=MESSAGE_PHONE_REGEX.format(LEN_PHONE)
    )

    @classmethod
    def validate_phone(cls, value):
        cls.regex_validator(value)
        cls.phone_max_length(value)
        cls.phone_min_length(value)


class NameFeedbackUserkValidator:
    '''Валидация имени в обращении обратной связи на длину и кириллицу.'''

    name_regex = RegexValidator(
        regex=r'^[а-яА-ЯёЁ\-]+$',
        message=MESSAGE_NAME_FEEDBACK_CYRILLIC
    )
    name_max_length = MaxLengthValidator(
        MAX_LEN_NAME_FEEDBACK,
        message=MESSAGE_NAME_FEEDBACK_VALID
    )
    name_min_length = MinLengthValidator(
        MIN_LEN_NAME_FEEDBACK,
        message=MESSAGE_NAME_FEEDBACK_VALID
    )

    @classmethod
    def validate_name(cls, value):
        cls.name_regex(value)
        cls.name_max_length(value)
        cls.name_min_length(value)


class TextFeedbackValidator:
    '''Валидация текста в форме обратной связи на длину.'''

    text_max_length = MaxLengthValidator(
        MAX_LEN_TEXT_FEEDBACK,
        message=MESSAGE_TEXT_FEEDBACK_VALID
    )
    text_min_length = MinLengthValidator(
        MIN_LEN_TEXT_FEEDBACK,
        message=MESSAGE_TEXT_FEEDBACK_VALID
    )

    @classmethod
    def validate_text(cls, value):
        cls.text_max_length(value)
        cls.text_min_length(value)
