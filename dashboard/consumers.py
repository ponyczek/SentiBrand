import json
import os
import threading

import tweepy
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.generic.websockets import WebsocketDemultiplexer
# from .tasks import hello_world
from SentiBrand.celery import app

# from __future__ import absolute_import
import json
import tweepy
import os

from channels import Channel, Group

consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



@channel_session_user_from_http
def ws_connect(message):
    group_name = message.user.username + "_search"
    print("Connect:" + group_name)
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })
    # Group(group_name).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group('dashboard').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    group_name = message.user.username + "_search"
    # print(threading._active)
    # threading._active.get(group_name).cancel()

    Group(group_name).discard(message.reply_channel)

    print('disconnected')


@channel_session_user
def ws_receive(message):
    try:
        data = json.loads(message['text'])
        print(data)
    except ValueError:
        # log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name
        get_search_data(data, reply_channel)



consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_search_data(message, reply_channel):
    if message is not None and reply_channel is not None:
        query_phrase = message['text']
        last_id = message.get('last_tweet_id')
        temp_tweets = api.search(q=query_phrase, since_id=last_id)
        tweets = [tweet._json for tweet in temp_tweets ]

        Channel(reply_channel).send({"text": json.dumps(tweets)})