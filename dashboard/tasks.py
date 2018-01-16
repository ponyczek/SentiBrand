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

        get_search_data(message,reply_channel)


def get_search_data(message, reply_channel):
    # print("hi from task")
    # print(message)
    # if message is not None and reply_channel is not None:
    print(type(message))
    if message.get('last_tweet_id'):
        print('test')
        print(message['last_tweet_id'])
        query_phrase = message['text']
        # group_name = message['user_name'] + "_search"
        temp_tweets = api.search(q=query_phrase, since_id=message['last_tweet_id'])
        tweets = [tweet._json for tweet in temp_tweets ]
        Channel(reply_channel).send({"text": json.dumps(tweets)})
    else:
        # print(message['last_tweet_date'])
        query_phrase = message['text']
        # group_name = message['user_name'] + "_search"
        temp_tweets = api.search(q=query_phrase)
        tweets = [tweet._json for tweet in temp_tweets ]

        Channel(reply_channel).send({"text": json.dumps(tweets)})
