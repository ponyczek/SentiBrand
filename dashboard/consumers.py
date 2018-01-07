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
import time


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


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      # self.query = query
      self.thread = threading.Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = threading.Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()


def hello_world(query_phrase):
    tweets = api.search(q=query_phrase)
    status = tweets[0]
    Group('dashboard').send({"text": json.dumps(status._json)})
    print(status)
    # return status

t = perpetualTimer(2, lambda: hello_world("") )

# t = perpetualTimer(2, hello_world)
# print("hi")
# t.start()

@channel_session_user_from_http
def ws_connect(message):
    print("connected")

    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })
    Group('dashboard').add(message.reply_channel)


@channel_session
def ws_receive(message):
    try:
        print('kek')
        data = json.loads(message['text'])
        t = perpetualTimer(2, lambda: hello_world(data['text']))
        t.start()
        # print(data['text'])
    except ValueError:
       print("ws message isn't json text=%s", message['text'])
       return



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
    t.cancel()
    print('disconnected')
