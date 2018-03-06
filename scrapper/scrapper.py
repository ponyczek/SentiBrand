import json
import tweepy
import os
from textblob import TextBlob
from channels import Channel
from scrapper.models import Tweet, Search
from dateutil import parser

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
        polarity = TextBlob(tweet.get('full_text'))
        lat, lng = get_lat_len(tweet)
        data.append({
            'text': tweet.get('full_text'),
            'user': tweet.get('user'),
            'polarity': polarity.sentiment.polarity,
            'lat': lat,
            'lng': lng,
            'created_at': tweet.get('created_at'),
            'profile_image_url' : tweet.get('profile_image_url'),
            'id' : tweet.get('id'),
        })
    return data

def create_tweet_records(tweets, search_record):
    for tweet in tweets:
        result = Tweet()
        result.tweet_id = tweet.get('id')
        try:
            Tweet.objects.get(tweet_id=result.tweet_id)
        except Tweet.DoesNotExist:
            polarity = TextBlob(tweet.get('full_text'))
            result.polarity = polarity.sentiment.polarity
            result.lat, result.lng = get_lat_len(tweet)
            result.content = tweet.get('full_text')
            result.created_at = parser.parse(tweet.get('created_at'))
            result.profile_image_url = tweet.get('user').get('profile_image_url_https')
            result.username = tweet.get('user').get('name')
            result.save()
            result.search_id.add(search_record)

    return tweets[0].get('id')

def handle_api_call(query_phrase, last_id):
    temp_tweets = api.search(q=query_phrase, since_id=last_id, lang='en', count=100, tweet_mode='extended')
    return [tweet._json for tweet in temp_tweets]

def get_search_data(message, reply_channel):
    if message is not None and reply_channel is not None:
        query_phrase = message['text']
        last_id = message.get('last_tweet_id')
        tweets = handle_api_call(query_phrase, last_id)
        data = serialise_data(tweets)
        Channel(reply_channel).send({"text": json.dumps(data)})

def get_lat_len(tweet):
    if tweet.get('geo'):
        geo = tweet.get('geo')
        return geo.get('coordinates')[0], geo.get('coordinates')[1]
    elif tweet.get('place'):
        place = tweet.get('place')
        return place.get('bounding_box').get('coordinates')[0][0][1], place.get('bounding_box').get('coordinates')[0][0][0]
    else:
        return None, None