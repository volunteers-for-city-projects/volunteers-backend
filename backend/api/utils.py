from djoser.compat import get_user_email
from djoser.conf import settings


def create_user(self, serializer, data):
    user_serializer = serializer(data=data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(
                self.context.get('request'), context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(
                self.context.get('request'), context).send(to)
    return user
