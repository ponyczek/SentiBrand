from channels.auth import channel_session_user, channel_session_user_from_http

import json
import tweepy
import os
from textblob import TextBlob

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

def serialise_data(tweets):
    data = []
    for tweet in tweets:
        polarity = TextBlob(tweet.get('text'))
        data.append({
            'text': tweet.get('text'),
            'user': tweet.get('user'),
            'polarity': polarity.sentiment.polarity,
            'geolocation': tweet.get('geo'), #exact location
            'created_at': tweet.get('created_at'),
            'profile_image_url' : tweet.get('profile_image_url'),
            'id' : tweet.get('id'),
            'place': tweet.get('place'), #city country coordinates
        })

    return data
        # data.append


def get_search_data(message, reply_channel):
    if message is not None and reply_channel is not None:
        query_phrase = message['text']
        last_id = message.get('last_tweet_id')
        temp_tweets = api.search(q=query_phrase, since_id=last_id, lang='en', count=100)
        tweets = [tweet._json for tweet in temp_tweets ]
        data = serialise_data(tweets)
        Channel(reply_channel).send({"text": json.dumps(data)})