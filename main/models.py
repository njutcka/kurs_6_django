from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='фио_клиента')
    email = models.EmailField(max_length=50, verbose_name='почта', unique=True)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ('email',)


class Msg(models.Model):
    msg_title = models.CharField(max_length=25, verbose_name='Тема письма')
    msg_body = models.TextField(verbose_name='Текст письма')

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.msg_title}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ('msg_title',)


class Mailing(models.Model):
    DAILY = "Ежедневная"
    WEEKLY = "Еженедельная"
    MONTHLY = "Ежемесячная"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]
    title_mail = models.CharField(max_length=25, verbose_name='Название рассылки', **NULLABLE)
    period_mail = models.CharField(max_length=25, choices=PERIODICITY_CHOICES, verbose_name='Периодичность рассылки')
    status_mail = models.CharField(max_length=25, choices=STATUS_CHOICES,
                                   verbose_name='Статус рассылки')  # создана, запущена, выполнена
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    client = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Msg, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.title_mail}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ('period_mail',)


class Logfile(models.Model):
    STATUS_CHOICES = [
        ('SENT', 'Отправлено'),
        ('FAILED', 'Не удалось отправить'),
    ]

    time_log = models.DateTimeField(default=timezone.now, verbose_name='дата и время последней попытки')
    status_log = models.BooleanField(verbose_name='статус попытки', choices=STATUS_CHOICES, default='SENT')
    server_response = models.CharField(max_length=100, verbose_name='ответ почтового сервера', **NULLABLE)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f"{self.time_log} {self.status_log}"

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"
        ordering = ('status_log',)
