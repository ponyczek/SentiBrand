CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379/1'

# from django.apps import apps
from datetime import timedelta
from celery import Celery
from celery.task.base import periodic_task
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SentiBrand.settings")
django.setup()
from dashboard.models import UserPhrase
from scrapper.models import Search, Tweet
import datetime
from scrapper.scrapper import handle_api_call, create_tweet_records

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER = True
app = Celery('taskscheduler', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@periodic_task(run_every=timedelta(seconds=60))
def get_tweets():

    user_phrases = UserPhrase.objects.all() #This can be improved bt using action manager
    search_date = datetime.datetime.now()
    for user_phrase in user_phrases:
        if user_phrase.is_active:
            search_record = Search(user_phrase=user_phrase, created_at=search_date) #must be changed to user_phrase
            search_record.save() #created search Record
            searched_phrase = user_phrase.phrase.phrase
            tweets = handle_api_call(searched_phrase, user_phrase.last_tweet_id)
            if(len(tweets) > 0):
                user_phrase.last_tweet_id =  create_tweet_records(tweets, search_record) #this function that creates all tweets and returns the last tweet id
                user_phrase.save()