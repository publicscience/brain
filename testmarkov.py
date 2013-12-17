from app.brain import twitter, _get_tweet_texts
from app.brain.markov import Markov

foo = twitter.tweets('frnsys', count=2000)
t = _get_tweet_texts(foo)
m = Markov(ramble=True, ngram_size=2)
m.train(t)
for i in range(10):
    print(m.generate())