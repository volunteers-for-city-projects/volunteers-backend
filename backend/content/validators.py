from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)

from backend.settings import (
    LEN_PHONE,
    MAX_LEN_NAME_FEEDBACK,
    MAX_LEN_TEXT_FEEDBACK,
    MAX_LENGTH_EMAIL,
    MESSAGE_EMAIL_VALID,
    MESSAGE_NAME_FEEDBACK_CYRILLIC,
    MESSAGE_NAME_FEEDBACK_VALID,
    MESSAGE_PHONE_REGEX,
    MESSAGE_TEXT_FEEDBACK_VALID,
    MIN_LEN_NAME_FEEDBACK,
    MIN_LEN_TEXT_FEEDBACK,
    MIN_LENGTH_EMAIL,
)


class EmailValidator:
    email_max_length = MaxLengthValidator(
        MAX_LENGTH_EMAIL,
        message=MESSAGE_EMAIL_VALID
    )
    email_min_length = MinLengthValidator(
        MIN_LENGTH_EMAIL,
        message=MESSAGE_EMAIL_VALID
    )

    @classmethod
    def validate_email(cls, value):
        cls.email_max_length(value)
        cls.email_min_length(value)


class PhoneValidator:
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
