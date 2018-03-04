# from __future__ import absolute_import

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379/1'
import os
import django
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentiBrand.settings')
# Setup django project
django.setup()

from django.apps import apps
from datetime import timedelta
from celery import Celery
from celery.task.base import periodic_task
from dashboard.models import User_Phrase
from scrapper.scrapper import get_search_data
# timezone = 'Europe/London'

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
app = Celery('taskscheduler', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@periodic_task(run_every=timedelta(seconds=5))
def get_all_tweets():
    # user_phrases = User_Phrase.objects.all()
    print('test')
    # for user_phrase in user_phrases:
    #     #check if this search is active
    #     # s
    #     searched_phrase = user_phrases.is_avtive()
    #
    #     print(user_phrases.is_active())