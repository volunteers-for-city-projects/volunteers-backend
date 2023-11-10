import re

from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.utils.regex_helper import _lazy_re_compile

from backend.settings import (
    MAX_LEN_NAME_USER,
    MAX_LENGTH_EMAIL_USER_PART,
    MESSAGE_EMAIL_NOT_VALID,
    MESSAGE_EMAIL_USER_PART_VALID,
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


class PasswordMaximumLengthValidator:
    """
    Проверка максимальной длинны вводимого пароля.
    """

    def __init__(self, max_length=20):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                (
                    'Пароль слишком длинный. Максимальная длинна: '
                    '%(max_length)s символов.' % {
                        'max_length': self.max_length}
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return (
            'Пароль слишком длинный. Максимальная длинна: '
            '%(max_length)s символов.' % {'max_length': self.max_length}
        ),


class PasswordRegexValidator:
    """
    Проверка вводимого пароля на соответствие регулярному выражению.
    """

    def __init__(self, regex=None):
        self.regex = _lazy_re_compile(regex, re.IGNORECASE)

    def validate(self, password, user=None):
        if self.regex is not None and not self.regex.match(password):
            raise ValidationError(
                (
                    "В пароле допускаются цифры, буквы и спецсимовлы "
                    "-!#$%&'*+/=?^_;():@,.<>`{}"
                ),
                code="password_incorect",
            )

    def get_help_text(self):
        return (
            "В пароле допускаются цифры, буквы и спецсимовлы "
            "-!#$%&'*+/=?^_;():@,.<>`{}"
        ),


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
            user_part, _ = value.rsplit("@", 1)
        except ValueError:
            raise ValidationError(MESSAGE_EMAIL_NOT_VALID)
        cls.email_max_length(user_part)
