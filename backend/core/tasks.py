from celery import shared_task
from mail_templated import send_mail


@shared_task
def send_email_task(template_name, context, from_email, recipient_list):
    """Таска на отправку сообщений через SMTP или gmail"""
    send_mail(template_name, context, from_email, recipient_list)
