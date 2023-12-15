from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

from main.models import Logfile


def send_mailing(mailing):
    now = timezone.localtime(timezone.now())
    if mailing.start_to_send <= now <= mailing.stop_to_send:
        for client in mailing.client.all():
            try:
                send_mail(
                    mailing.message.msg_title,
                    mailing.message.msg_body,
                    settings.EMAIL_HOST_USER,
                    recipient_list=[client],
                    fail_silently=False
                )
                log = Logfile.objects.create(
                    last_try=mailing.start_time,
                    status_try='Успешно',
                    mailling=mailing,
                    client=client.email
                )
                log.save()
                return log

            except SMTPException as error:
                log = Logfile.objects.create(
                    last_try=mailing.end_time,
                    status_try='Ошибка',
                    mailling=mailing,
                    client=client.email,
                    answer=error
                )
                log.save()
                return log