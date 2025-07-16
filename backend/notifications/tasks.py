from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from djoser.compat import get_user_email

from .email import IncomesApproveEmail, IncomesRejectEmail

User = get_user_model()


@shared_task
def incomes_approve_send_email(instance_pk, ctx):
    from projects.models import ProjectParticipants  # noqa
    date_time = timezone.now()
    instance = ProjectParticipants.objects.filter(
        pk=instance_pk).select_related('volunteer__user', 'project').first()
    ctx.update({
        'user': instance.volunteer.user,
        'project': instance.project,
        'date_time': date_time,
    })
    to = [get_user_email(instance.volunteer.user)]
    IncomesApproveEmail(context=ctx).send(to)


@shared_task
def incomes_reject_send_email(instance_pk, ctx):
    from projects.models import ProjectParticipants  # noqa
    date_time = timezone.now()
    instance = ProjectParticipants.objects.filter(
        pk=instance_pk).select_related('volunteer__user', 'project').first()
    ctx.update({
        'user': instance.volunteer.user,
        'project': instance.project,
        'date_time': date_time,
    })
    to = [get_user_email(instance.volunteer.user)]
    IncomesRejectEmail(context=ctx).send(to)
