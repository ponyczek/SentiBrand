import json
import os
import threading

import tweepy
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.generic.websockets import WebsocketDemultiplexer
from .tasks import hello_world
from SentiBrand.celery import app

consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# class perpetualTimer():
#     def __init__(self, t, hFunction, thread_name):
#         self.t = t
#         self.hFunction = hFunction
#         self.thread_name = thread_name
#         self.thread = threading.Timer(self.t, self.handle_function)
#         print(thread_name)
#         self.thread.setName(thread_name)
#
#     def handle_function(self):
#         self.hFunction()
#         self.thread = threading.Timer(self.t, self.handle_function)
#         self.thread.start()
#
#     def start(self):
#         self.thread.start()
#
#     def cancel(self):
#         self.thread.cancel()


# class WsThread(WebsocketDemultiplexer):
#     http_user = True
#
#     def connection_groups(self, **kwargs):
#         pass
#
#     def receive(self, message, **kwargs):
#         try:
#             thread_name = message['user_name'] + "_search"
#             t = perpetualTimer(2, lambda: hello_world(message), thread_name )
#             t.start()
#         except ValueError:
#             print("ws message isn't json text=%s", message['text'])
#             return


# def hello_world(message):
#     query_phrase = message['text']
#     group_name = message['user_name'] + "_search"
#     tweets = api.search(q=query_phrase)
#     status = tweets[0]
#     Group(group_name).send({"text": json.dumps(status._json)})
#     print(status)


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
        # reply_channel = message.reply_channel.name
        #
        # if data['action'] == "start_sec3":
        print("call hello world")
        reply_channel = message.reply_channel.name
        hello_world(data, reply_channel)


# def start_hello_world(message, reply_channel):
    # print("hello from start")

    # Start long running task here (using Celery)
    # sec3_task = \
    # hello_world(message)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    # job.celery_id = sec3_task.id
    # job.save()

    # Tell client task has been started
    # Channel(reply_channel).send({
    #     "text": json.dumps({
    #         "action": "started",
    #         "job_id": job.id,
    #         "job_name": job.name,
    #         "job_status": job.status,
    #     })
    # })