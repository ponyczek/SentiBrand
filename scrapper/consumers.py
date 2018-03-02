from channels.auth import channel_session_user, channel_session_user_from_http
import json
from scrapper.scrapper import  get_search_data
from channels import  Group

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
    print('disconnected')


@channel_session_user
def ws_receive(message):
    try:
        data = json.loads(message['text'])
        print(data)
    except ValueError:
        return

    if data:
        reply_channel = message.reply_channel.name
        get_search_data(data, reply_channel)

