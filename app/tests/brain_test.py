import unittest
from unittest.mock import MagicMock
from app import brain
from . import RequiresMocks

class BrainTest(RequiresMocks):
    def setUp(self):
        self.mock_twitter = self.create_patch('app.brain.twitter')
        self.mock_Tweet = self.create_patch('app.brain.Tweet')
        self.mock_CLS = self.create_patch('app.brain.CLS')

        # Mock the app config.
        self.faux_config = MagicMock()
        self.faux_config.retweet_threshold = 0.9
        self.faux_config.max_retweets = 10
        self.mock_config = self.create_patch('app.brain.config')
        self.mock_config.return_value = self.faux_config

        self.faux_tweets = [{
            'body': 'hey there',
            'tid': 1234,
            'protected': False,
            'retweeted': False
        }]

    def tearDown(self):
        pass

    def test_process_muse_creates_Tweets(self):
        muse = MagicMock(name='muse')
        muse.username = 'foo'
        self.mock_twitter.tweets.return_value = self.faux_tweets

        brain._process_muse(muse)

        self.mock_Tweet.assert_called_with(body='hey there', tid=1234, username='foo')

    def test_consider_retweets_above_threshold_does_retweet(self):
        self.mock_CLS.classify.return_value = [[0,1]]
        brain._consider_retweets(self.faux_tweets)
        self.mock_twitter.retweet.assert_called_with(1234)

    def test_consider_retweets_below_threshold_does_not_retweet(self):
        self.mock_CLS.classify.return_value = [[1,0]]
        brain._consider_retweets(self.faux_tweets)
        self.assertFalse(self.mock_twitter.retweet.called)

    def test_consider_retweets_max_retweets_does_not_retweet(self):
        self.faux_config.max_retweets = 0
        self.mock_CLS.classify.return_value = [[0,1]]
        brain._consider_retweets(self.faux_tweets)
        self.assertFalse(self.mock_twitter.retweet.called)

    def test_consider_retweets_already_retweeted_does_not_retweet(self):
        self.faux_tweets[0]['retweeted'] = True
        self.mock_CLS.classify.return_value = [[0,1]]
        brain._consider_retweets(self.faux_tweets)
        self.assertFalse(self.mock_twitter.retweet.called)

    def test_consider_retweets_protected_does_not_retweet(self):
        self.faux_tweets[0]['protected'] = True
        self.mock_CLS.classify.return_value = [[0,1]]
        brain._consider_retweets(self.faux_tweets)
        self.assertFalse(self.mock_twitter.retweet.called)


if __name__ == '__main__':
    unittest.main()
