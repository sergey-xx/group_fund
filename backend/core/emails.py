from django.conf import settings
from .tasks import send_email_task

def send_collect_confirm(collect):
    """Оправка уведомления о проверки документов."""
    last_name = collect.author.last_name
    first_name = collect.author.first_name
    title = collect.title
    send_email_task.delay(
        'mail/collect_create_confirm.html',
        {
            'last_name': last_name,
            'first_name': first_name,
            'title': title
        },
        settings.EMAIL_HOST_USER,
        [collect.author.email]
    )
