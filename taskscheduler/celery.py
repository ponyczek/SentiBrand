CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379/1'
from django.apps import apps
from datetime import timedelta
from celery import Celery
from celery.task.base import periodic_task


CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
app = Celery('taskscheduler', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@periodic_task(run_every=timedelta(seconds=5))
def just_print():
    print("Print from celery task")