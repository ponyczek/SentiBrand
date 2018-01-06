from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http, channel_session
import json
import scrapper
import tweepy
import os
import time
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import threading

consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status)
        return True

    def on_data(self, tweet):
        # data = json.loads(HTMLParser().unescape(data))
        # s = SessionStore()
        print("bla" + str(type(tweet)))
        # Group('dashboard').send({'text': tweet})
        # print(s)
        # data = json.loads(tweet)
        # return json.loads(tweet)

        # return True


# def send_notification(notification):
    # Group('notifications').send({'text': json.dumps(notification)})

# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
# myStream.disconnect()
# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

def hello_world():
    tweets = api.search(q='goodnight')
    status = tweets[0]
    threading.Timer(2.0, hello_world).start()
    print(status._json);
    Group('dashboard').send({"text": json.dumps(status._json)})
    # return status

@channel_session_user_from_http
def ws_connect(message):
    hello_world()
    # tweets = api.search(q='goodnight')
    # status = tweets[0]
    # myStreamListener = MyStreamListener()
    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # myStream.disconnect()

    # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # myStream.filter(track=['goodnight'], async=True)
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })
    Group('dashboard').add(message.reply_channel)


    # tweets = api.search(q='goodnight')
    # status = tweets[0]
    # print(status)
    #
    # # myStreamListener = MyStreamListener()
    # # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # # output = myStream.filter(track=['goodnight'], async=True)
    # Group('dashboard').add(message.reply_channel)
    # Group('dashboard').send({
    #     'text': json.dumps(status._json)
    # })
    # Group('dashboard').send({
    #     'text': json.dumps(status._json)
    # })
    # Group('dashboard').send({
    #     'text': json.dumps(status._json)
    # })
@channel_session
def ws_receive(message):
    print("is it ever called")
    try:
        data = json.loads(message['text'])
    except ValueError:
       print("ws message isn't json text=%s", message['text'])
       return
    if data:
       reply_channel = message.reply_channel.name
       if data['action'] == "start_sec3":
           print(data, reply_channel)

@channel_session_user
def ws_disconnect(message):
    Group('dashboard').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('dashboard').discard(message.reply_channel)
    # myStream.disconnect()
    print('disconnected')
