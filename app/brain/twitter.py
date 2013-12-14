import tweepy

import os
import simplejson as json
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def api():
    # Load auth info from config.
    # Setup things on Twitter's end at:
    # https://dev.twitter.com/apps
    config = json.loads( open(os.path.join(__location__, 'config.json')).read() )
    twitter = config['twitter']
    auth = tweepy.OAuthHandler(twitter['consumer_key'], twitter['consumer_secret'])
    auth.set_access_token(twitter['access_token'], twitter['access_token_secret'])

    # Return API object.
    return tweepy.API(auth)
