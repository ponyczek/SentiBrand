# import twitter
# import os
#
# consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
# consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
# access_token = os.environ.get('SENTI_ACCESS_TOKEN')
# access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')
#
# api = twitter.Api(consumer_key=[consumer_key],
#                   consumer_secret=[consumer_secret],
#                   access_token_key=[access_token],
#                   access_token_secret=[access_token_secret])
#
# def get_tweets():
#     """
#     returns twitter feed with settings as described below, contains all related twitter settings
#     """
#     # print(sys.stderr, 'hi')
#     # print(sys.stderr, api.GetUserTimeline(screen_name='AdrianPonczek', exclude_replies=True, include_rts=False))
#     return api.GetUserTimeline(screen_name='@AdrianPonczek', exclude_replies=True, include_rts=False)  # includes entities

import tweepy
import os
consumer_key = os.environ.get('SENTI_CONSUMER_KEY')
consumer_secret = os.environ.get('SENTI_CONSUMER_SECRET')
access_token = os.environ.get('SENTI_ACCESS_TOKEN')
access_token_secret = os.environ.get('SENTI_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)


# public_tweets = api.home_timeline()
public_tweets = api.search(q='trump')

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


def get_tweets(query):
    tweets = api.search(q=query)

    # myStreamListener = MyStreamListener()
    # myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    # return myStream.filter(track=['python'], async=True)
    return tweets