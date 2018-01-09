from __future__ import absolute_import
import time
import json
import logging
import tweepy
import os
from datetime import timedelta

from SentiBrand.celery import app
from celery.task import periodic_task
from celery.schedules import crontab
from channels import Channel, Group
# from celery.task import periodic_task


log = logging.getLogger(__name__)

consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 3 seconds.
#     sender.add_periodic_task(3.0, test.s('hello'), name='add every 10')

# @app.task(run_every=timedelta(seconds=5))
@periodic_task(run_every=crontab(minute=1))
def hello_world(message, reply_channel):
    print("hi from task")
    print(message)
    if message is not None and reply_channel is not None:
        # query_phrase = message['text']
        # # group_name = message['user_name'] + "_search"
        # tweets = api.search(q=query_phrase)
        # status = tweets[0]
        # # print(group_name)
        # print(json.dumps(status._json))
        #
        # Channel(reply_channel).send({"text": json.dumps(status._json)})
        # # print(status)
        # test(message,reply_channel)
        # while True:
        get_search_data(message,reply_channel)
        # return True
        # return True
        # return True


    # else:
        # print("test")
        # return True
        # return True

def get_search_data(message, reply_channel):
    # print("hi from task")
    # print(message)
    # if message is not None and reply_channel is not None:
    query_phrase = message['text']
    # group_name = message['user_name'] + "_search"
    tweets = api.search(q=query_phrase)
    status = tweets[0]
    # print(group_name)
    print(json.dumps(status._json))

    Channel(reply_channel).send({"text": json.dumps(status._json)})
    # time.sleep(3)

    # hello_world(message,reply_channel)
    # return True

    # return True

    # print(status)
    # time.sleep(3)
    # hello_world(message,reply_channel)
    # return True
    # else:
    #     return True