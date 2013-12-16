from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string, sys

class Markov():
    """
    Notes:
    –  to enforce max length, at max-length-1 should search for a word that has a high probability of being followed with stop?
    """

    def __init__(self, ngram_size=3, start_token='<START>', stop_token='<STOP>', max_tokens=10):
        self.n = ngram_size
        self.stop_token = stop_token
        self.start_token = start_token
        self.max_tokens = max_tokens

        # Load knowledge into memory.
        # For now, just start with nothing.
        # In the format of:
        # ('this', 'is', 'an'): [1, 'example']
        self.knowledge = {}

    def train(self, docs):
        """
        Add to knowledge the learnings
        from some input docs.
        """
        def stop_rule(token):
            # Ignore @ mentions
            if token[0] == '@':
                return True
            # Ignore 'RT' in retweets
            if token == 'RT':
                return True

        for doc in docs:
            # No stop words because all words are game for chain generation.
            tokens = self.tokenize(doc, stop_words=None, stop_rule=stop_rule)

            # Example, where ngram_size=3:
            # ngram = ['this', 'is', 'an', 'example']
            for ngram in self.ngramize(tokens):
                # The tokens leading up to the 'post'.
                # e.g. ('this', 'is', 'an')
                prior = tuple(ngram[:self.n])

                # The 'post' token.
                # e.g. 'example'
                post = ngram[-1]

                # Get existing data, if it's there.
                # Keeps track as:
                # prior: [count, {post: count}]

                # Create new prior entry if necessary.
                if prior not in self.knowledge:
                    self.knowledge[prior] = [0, {}]

                # Increment count of this prior
                self.knowledge[prior][0] += 1

                # Create new token entry for this prior
                # if necessary.
                if post not in self.knowledge[prior][1]:
                    self.knowledge[prior][1][post] = 0

                # Increment count of this post token
                # for this prior
                self.knowledge[prior][1][post] += 1

    def ngramize(self, tokens):
        """
        A generator which chunks a list of tokens
        into ngram lists.
        """

        # Ensure we have enough tokens to work with.
        if len(tokens) > self.n:
            # Add the <start> token to the beginning,
            # and the <stop> token to the end.
            tokens.insert(0, self.start_token)
            tokens.append(self.stop_token)

            # Yield the ngrams.
            for i in range(len(tokens) - self.n):
                next = i + self.n + 1
                yield tokens[i:next]

    def tokenize(self, doc, stop_words='default', stop_rule=lambda token: False):
        """
        Tokenizes a document.

        Optionally provide a `stop_rule` function,
        which should return True if a token should be stopped on.
        """
        tokens = []
        if stop_words == 'default':
            stops = set(list(string.punctuation) + stopwords.words('english'))
        elif stop_words is None:
            stops = []
        else:
            stops = stop_words

        # Tokenize
        for sentence in sent_tokenize(doc):
            for token in word_tokenize(sentence):

                # This saves memory by having
                # duplicate strings just point to the same memory.
                token = sys.intern(token)

                # Ignore punctuation and stopwords
                if token in stops or stop_rule(token):
                    continue
                tokens.append(token)
        return tokens

    def generate(self, seed):
        tokens = []

        for i in range(self.max_tokens):
            seed_tokens = self.tokenize(seed)
            tokens.append(seed_tokens[0])
            next_token = None # roll for the next word that follows

            # If a word couldn't be found, stop.
            if not next_token:
                break

            # Generate new seed.
            seed = seed_tokens[1:] + [next_token]

        return ' '.join(tokens)