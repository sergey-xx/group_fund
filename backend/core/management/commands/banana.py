from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings

from core.emails import (send_collect_confirm,)
from django.core.files.images import ImageFile
from funds.models import Collect

User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        collect = Collect.objects.first()
        send_collect_confirm(collect)
