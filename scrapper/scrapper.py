import tweepy
import os
import json

consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)


# public_tweets = api.home_timeline()
# public_tweets = api.search(q='trump')

# streamer = Streamer(auth, callback)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status)
        return True

    def on_data(self, tweet):
        return  json.loads(tweet)
    # def on_data(self, status):
    #     self.output[status.id] = {
    #
    #     }
    #
    #     return True

def get_tweets(query):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=[query], async=True)
    # print(myStream.filter(track=[query], async=True))
    tweets = api.search(q=query)

    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # return myStream.filter(track=['python'], async=True)
    return tweets