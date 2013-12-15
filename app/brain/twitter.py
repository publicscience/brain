import tweepy

from os import getcwd, path
import simplejson as json
__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))

def _api():
    """
    Load auth info from config.
    Setup things on Twitter's end at:
    https://dev.twitter.com/apps
    """
    config = json.loads( open(path.join(__location__, 'config.json')).read() )
    twitter = config['twitter']
    auth = tweepy.OAuthHandler(twitter['consumer_key'], twitter['consumer_secret'])
    auth.set_access_token(twitter['access_token'], twitter['access_token_secret'])

    # Return API object.
    return tweepy.API(auth)

api = _api()

def tweets(username):
    """
    Returns 200 last tweets for a user.
    """
    return [
            {
                'body': tweet.text.encode('utf-8'),
                'id': tweet.id
            }
            for tweet in api.user_timeline(screen_name=username, count=200)
            ]

def retweet(id):
    api.retweet(id)