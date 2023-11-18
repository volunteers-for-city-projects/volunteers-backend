
from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import SendEmailResetSerializer, TokenCreateSerializer
from rest_framework.validators import ValidationError

from api.mixins import IsValidModifyErrorForFrontendMixin

User = get_user_model()


class CustomTokenCreateSerializer(IsValidModifyErrorForFrontendMixin,
                                  TokenCreateSerializer):
    """
    Класс создания токена для аутентификации с переопределенным методом
    валидации принимаемых данных.
    Проверяется:
        - существование логина
        - соответствие пароля
        - активирован ли аккаунт
    """

    default_error_messages = {
        'inactive_account': settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
        'missing_account': settings.CONSTANTS.messages.EMAIL_NOT_FOUND,
        'wrong_password': settings.CONSTANTS.messages.INVALID_PASSWORD_ERROR,
    }

    def validate(self, attrs):
        class_name = self.__class__.__name__
        password = attrs.get('password')
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = User.objects.filter(**params).first()
        if not self.user:
            raise ValidationError(
                {
                    class_name: {
                        settings.LOGIN_FIELD:
                        [self.default_error_messages.get('missing_account')]
                    }
                }, code='not_exist'
            )
        elif not self.user.check_password(password):
            raise ValidationError(
                {
                    class_name: {
                        'password':
                        [self.default_error_messages.get('wrong_password')]
                    }
                }, code='wrong'
            )
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )
        if self.user and self.user.is_active:
            return attrs
        raise ValidationError(
            {
                class_name: {
                    'not_active':
                    [self.default_error_messages.get('inactive_account')]
                }
            }, code='wrong'
        )


class CustomSendEmailResetSerializer(IsValidModifyErrorForFrontendMixin,
                                     SendEmailResetSerializer):
    """
    Класс отправки ссылки для сброса пароля.
    Переопределен метод получения пользователя. Возбуждается ошибка валидации
    со структурой деталей ошибки более удобной для фронтов.
    """

    def get_user(self, is_active=True):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        if (
            settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
            or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            class_name = self.__class__.__name__
            raise ValidationError(
                {
                    class_name: {
                        settings.LOGIN_FIELD:
                        [self.default_error_messages.get('email_not_found')],
                        'ValidationErrors': {}
                    },
                }
            )
