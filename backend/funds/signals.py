from django.dispatch import receiver
from django.db.models.signals import post_save

from core.emails import send_collect_confirm
from .models import Collect


@receiver(post_save, sender=Collect)
def collect_notification(sender, instance, created, **kwargs):
    """Отправляет уведомления о регистрации и проверке документов."""
    send_collect_confirm(instance)
