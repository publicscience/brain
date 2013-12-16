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
    """

    # Retweet probability threshold.
    retweet_threshold = db.FloatField(required=True, default=0.9)

    # Maximum activity (tweets + retweets) in the active time interval.
    max_activity = db.IntField(required=True, default=10)

    meta = {
            'max_documents': 1
    }
