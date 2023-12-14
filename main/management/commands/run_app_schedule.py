import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from main.services import send_mailing

from main.models import Mailing

logger = logging.getLogger(__name__)


def daily_tasks():
    mailings = Mailing.objects.filter(periodicity="DAILY", status=True)
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = Mailing.objects.filter(periodicity="WEEKLY", status=True)
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = Mailing.objects.filter(periodicity="MONTHLY", status=True)
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_tasks,
            trigger=CronTrigger(hour="*/10"),  # Every day
            id="daily_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'daily_job'.")

        scheduler.add_job(
            weekly_tasks,
            trigger=CronTrigger(day_of_week="*/1"),  # Every monday
            id="weekly_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_job'.")

        scheduler.add_job(
            monthly_tasks,
            trigger=CronTrigger(day="*/30"),  # Every month
            id="monthly_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'monthly_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")