from app.brain import twitter
from app.brain.classifier import Classifier
from app.brain.markov import Markov
from app.models import Muse, Tweet, Doc
from app.config import config
from mongoengine.errors import NotUniqueError
import random

# Logging
from app.logger import logger
logger = logger(__name__)

# Load the classifier and markov.
# Loaded here so we can keep it in memory.
# accessible via app.brain.CLS or app.brain.MKV
CLS = Classifier()
MKV = Markov(ramble=False)

def ponder():
    """
    Fetch tweets from the Muses
    and memorize them;
    i.e. train classifier or Markov on them.
    """
    logger.info('Pondering new twitter data...')

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

    # Combine the new tweets.
    new_tweets = pos_txts + neg_txts

    # Extract the tweet contents into lists.
    pos_txts = _get_tweet_texts(pos)
    neg_txts = _get_tweet_texts(neg)

    # Construct training matrix and labels.
    labels = [1 for i in range(len(pos_txts))] + [0 for i in range(len(neg_txts))]

    # See if there's anything to retweet.
    _consider_retweets(pos)

    # Update the classifier and markov.
    logger.info('Collected %s new tweets, training...' % len(new_tweets))
    CLS.train(new_tweets, labels)
    MKV.train(pos_txts)


def consider():
    """
    Decide whether or not to act (tweet).
    """
    logger.info('Considering tweeting...')
    roll = random.random()
    chance = config().chance_to_act
    if roll < chance:
        logger.info('Rolled %s, chance to act is %s, tweeting.' % (roll, chance))
        twitter.tweet(MKV.generate())
    else:
        logger.info('Rolled %s, chance to act is %s, NOT tweeting.' % (roll, chance))


def retrain():
    """
    Retrains the Markov generator on the documents in the database.
    """
    MKV.reset()
    MKV.train(Twitter.objects.all())
    MKV.train(Doc.objects.all())


def _process_muse(muse):
    """
    Processes a Muse's tweets,
    creating Tweet objects
    and saving them to the db.
    """
    username = muse.username
    logger.info('Collecting tweets for %s...' % username)
    tweets = twitter.tweets(username=username)
    new_tweets = []
    for tweet in tweets:
        data = {
                'body': tweet['body'],
                'tid': tweet['tid'],
                'username': username
        }
        t = Tweet(**data)
        try:
            t.save()
            new_tweets.append(tweet)
        except NotUniqueError:
            # Duplicate tweet
            pass
    return new_tweets


def _consider_retweets(tweets):
    """
    Retweets if positive
    classification is above THRESHOLD.
    0 = neg, 1 = pos
    """
    logger.info('Considering retweeting...')
    num_retweeted = 0
    retweet_threshold = config().retweet_threshold

    # Filter out protected tweets.
    candidates = [tweet for tweet in tweets if not tweet['protected'] and not tweet['retweeted']]
    txts = _get_tweet_texts(candidates)
    if txts:
        for idx, doc_probs in enumerate(CLS.classify(txts)):
            if num_retweeted >= config().max_retweets:
                logger.info('Hit maximum retweet limit, stopping for now.')
                break
            if doc_probs[1] > retweet_threshold:
                logger.info('Classified as %s retweetable, above %s threshold, retweeting...' % (doc_probs[1], retweet_threshold))
                twitter.retweet(candidates[idx]['tid'])
                num_retweeted += 1
            else:
                logger.info('Classified as %s retweetable, below %s threshold, not retweeting...' % (doc_probs[1], retweet_threshold))


def _get_tweet_texts(tweets):
    """
    Pulls out the content of a list of Tweets.
    """
    return [tweet['body'] for tweet in tweets]
