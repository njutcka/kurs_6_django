from smtplib import SMTPException

from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

from main.models import Logfile, Client, Msg


def get_cache_clients():
    if settings.CACHE_ENABLED:
        key = 'client_list'
        client_list = cache.get(key)
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
    else:
        client_list = Client.objects.all()
    return client_list


def get_cache_messages():
    if settings.CACHE_ENABLED:
        key = 'message_list'
        message_list = cache.get(key)
        if message_list is None:
            message_list = Msg.objects.all()
            cache.set(key, message_list)
    else:
        message_list = Msg.objects.all()
    return message_list


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