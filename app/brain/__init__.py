from app.brain import twitter
from app.brain.classifier import Classifier
from app.models import Muse, Tweet
from app.config import config

# Load the classifier.
# Loaded here so we can keep it in memory.
CLS = Classifier()

def ponder():
    """
    Fetch tweets from the Muses
    and memorize them,
    and decide how to act.
    """

    # Each of these are just a list
    # of tweets as strings.
    pos = []
    neg = []

    # For the good muses...
    for muse in Muse.objects(negative=False):
        pos += _process_muse(muse)

    # For the evil muses...
    for muse in Muse.objects(negative=True):
        neg += _process_muse(muse)

    # Extract the tweet contents into lists.
    pos_txts = _get_tweet_texts(pos)
    neg_txts = _get_tweet_texts(neg)

    # Construct training matrix and labels.
    labels = [1 for i in range(len(pos_txts))] + [0 for i in range(len(neg_txts))]

    # See if there's anything to retweet.
    _consider_retweets(pos)

    # Update the classifier.
    CLS.train(pos_txts + neg_txts, labels)


def _process_muse(muse):
    """
    Processes a Muse's tweets,
    creating Tweet objects
    and saving them to the db.
    """
    username = muse.username
    tweets = twitter.tweets(username=username)
    for tweet in tweets:
        data = {
                'body': tweet['body'],
                'tid': tweet['tid'],
                'username': username
        }
        t = Tweet(**data)
        t.save()
    return tweets

def _consider_retweets(tweets):
    """
    Retweets if positive
    classification is above THRESHOLD.
    0 = neg, 1 = pos
    """
    txts = _get_tweet_texts(tweets)
    for idx, doc_probs in enumerate(CLS.classify(txts)):
        if doc_probs[1] > config().threshold:
            twitter.retweet(tweets[idx]['tid'])


def _get_tweet_texts(tweets):
    """
    Pulls out the content of a list of Tweets.
    """
    return [tweet['body'] for tweet in tweets]
