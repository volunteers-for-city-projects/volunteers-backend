from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Organization, Volunteer

User = get_user_model()


@receiver(pre_delete, sender=Volunteer)
def delete_volunteer_photo(sender, instance, **kwargs):
    """
    Метод для предварительного удаления фотографии волонтера.
    """
    if instance.photo:
        instance.photo.delete(False)


@receiver(pre_delete, sender=Organization)
def delete_organization_photo(sender, instance, **kwargs):
    """
    Метод для предварительного удаления фотографии организации.
    """
    if instance.photo:
        instance.photo.delete(False)
