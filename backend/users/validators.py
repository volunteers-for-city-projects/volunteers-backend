from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            '"me" - запрещено использовать как имя пользователя'
        )
    return value
