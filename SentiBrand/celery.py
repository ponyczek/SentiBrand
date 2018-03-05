from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.task.base import periodic_task
from datetime import timedelta
# from dashboard.models import User_Phrase
# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentiBrand.settings')
# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SentiBrand.settings")
# django.setup()
app = Celery('SentiBrand')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


# @periodic_task(run_every=timedelta(seconds=5))
# def debug_task():
#     user_phrases = User_Phrase.objects.all()
#     print(user_phrases)