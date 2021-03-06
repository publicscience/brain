import datetime
from app import db

class Tweet(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    tid = db.IntField(required=True, unique=True)
    body = db.StringField(required=True, unique=True)
    username = db.StringField(required=True, max_length=50)

    meta = {
            'allow_inheritance': True,
            'indexes': ['-created_at', 'username'],
            'ordering': ['-created_at']
    }

class Muse(db.Document):
    """
    A muse is a Twitter user
    which the Brain learns from.
    """
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    username = db.StringField(required=True, unique=True, max_length=50)
    negative = db.BooleanField(default=False)

    meta = {
            'allow_inheritance': True,
            'indexes': ['-created_at', 'username'],
            'ordering': ['-created_at']
    }

class Config(db.Document):
    """
    Configuration for the Brain.

    If you make changes to this model,
    you will need to drop the saved record
    in the database.

    $ mongo
    > show dbs
    > use <your db>
    > db.config.drop()

    Then restart the application.
    """

    # Retweet probability threshold.
    # The higher this is, the less the brain will retweet.
    retweet_threshold = db.FloatField(required=True, default=0.9)

    # Chance to act. Probability the brain will tweet.
    # The lower this is, the less the brain will tweet.
    chance_to_act = db.FloatField(required=True, default=0.05)

    # Maximum amount of retweets in an interval.
    # Cause sometimes it accidentally retweets a TON of stuff.
    max_retweets = db.IntField(required=True, default=10)

    # Some brain configuration.
    ngram_size = db.IntField(required=True, default=1)
    ramble = db.BooleanField(default=True)
    spasm = db.FloatField(required=True, default=0.05)

    meta = {
            'max_documents': 1
    }

class Doc(db.Document):
    """
    A manually-fed training document for the Markov generator.
    """
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(required=True, unique=True)

    meta = {
            'allow_inheritance': True,
            'indexes': ['-created_at'],
            'ordering': ['-created_at']
    }
