from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from backend import celery_app

User = get_user_model()


@celery_app.task
def delete_not_active_users():
    tomorrow = timezone.now() - timezone.timedelta(days=1)
    with transaction.atomic():
        User.objects.filter(
            is_active=False,
            date_joined__lt=tomorrow,
        ).exclude(role=User.DELETED).delete()
