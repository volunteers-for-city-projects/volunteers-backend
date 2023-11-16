from django.contrib.auth import get_user_model
from django.db import transaction

from backend import celery_app

User = get_user_model()


@celery_app.task
def delete_not_active_users():
    with transaction.atomic():
        User.objects.filter(is_active=False).delete()
