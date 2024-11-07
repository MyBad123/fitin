from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(thema: str, text: str, mail: str | None = None):
    if mail:
        send_mail(
            thema, text,'your_email@yandex.ru',[mail],
            fail_silently=False,
        )
