from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from rest_framework.validators import ValidationError

User = get_user_model()


class CustomTokenCreateSerializer(TokenCreateSerializer):
    default_error_messages = {
        'inactive_account': settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
        'missing_account': settings.CONSTANTS.messages.EMAIL_NOT_FOUND,
        'wrong_password': settings.CONSTANTS.messages.INVALID_PASSWORD_ERROR,
    }

    def validate(self, attrs):
        password = attrs.get('password')
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = User.objects.filter(**params).first()
        if not self.user:
            raise ValidationError(
                {
                    settings.LOGIN_FIELD:
                    self.default_error_messages.get('missing_account')
                },
            )
        elif not self.user.check_password(password):
            raise ValidationError(
                {
                    'password':
                    self.default_error_messages.get('wrong_password')
                },
            )
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )
        if self.user and self.user.is_active:
            return attrs
        raise ValidationError(
            {
                'not_active':
                self.default_error_messages.get('inactive_account')
            },
        )
