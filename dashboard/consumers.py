from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http, channel_session
import json
import tweepy
import os
import threading
from channels.generic.websockets import WebsocketDemultiplexer


consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

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

class WsThread(WebsocketDemultiplexer):
    http_user = True

    def connection_groups(self, **kwargs):
        pass


    def receive(self, message, **kwargs):
        try:

            t = perpetualTimer(2, lambda: hello_world(message))
            t.start()
        except ValueError:
            print("ws message isn't json text=%s", message['text'])
            return


def hello_world(message):

    query_phrase = message['text']
    group_name = message['user_name'] + "_search"

    tweets = api.search(q=query_phrase)
    status = tweets[0]
    Group(group_name).send({"text": json.dumps(status._json)})
    print(status)

t = perpetualTimer(2, lambda: hello_world("") )


@channel_session_user_from_http
def ws_connect(message):
    group_name = message.user.username + "_search"
    message.reply_channel.send({
        "text": json.dumps({
            "action": "reply_channel",
            "reply_channel": message.reply_channel.name,
        })
    })
    Group(group_name).add(message.reply_channel)



@channel_session_user
def ws_disconnect(message):
    Group('dashboard').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    group_name = message.user.username + "_search"

    Group(group_name).discard(message.reply_channel)
    t.cancel()
    print('disconnected')
