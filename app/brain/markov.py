import string, sys
import random

class Markov():
    def __init__(self, ngram_size=3, stop_token='<STOP>', max_chars=140, ramble=False):
        self.n = ngram_size
        self.stop_token = stop_token
        self.max_chars = max_chars
        self.ramble = ramble

        # Load knowledge into memory.
        # For now, just start with nothing.
        # In the format of:
        # ('this', 'is', 'an'): [1, 'example']
        self.knowledge = {}

        # For keeping track of good starting tokens.
        # Starting tokens come after a prev value of (),
        # that is, after no previous tokens.
        self.knowledge[()] = {}

        # Keep track of the last ngram seen,
        # so we can pick the next token.
        self.prev = ()

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
            tokens = self.tokenize(doc, stop_rule=stop_rule)

            # Keep track of starting token candidates.
            start_token = tokens[0]
            self.knowledge[()][start_token] = self.knowledge[()].get(start_token, 0) + 1

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
            # Add the <stop> token to the end.
            tokens.append(self.stop_token)

            # Yield the ngrams.
            for i in range(len(tokens) - self.n):
                next = i + self.n + 1
                yield tokens[i:next]

    def tokenize(self, doc, stop_rule=lambda token: False):
        """
        Tokenizes a document.
        This is a very naive tokenizer;
        i.e. it has no stop words,
        since we need those words to generate convincing speech.
        It also strips punctuation from the beginning and end of tokens,
        except for '@' at the beginning of a token.

        Optionally provide a `stop_rule` function,
        which should return True if a token should be stopped on.
        """
        tokens = []
        punctuation = string.punctuation.replace('@', '')

        for token in doc.split(' '):
            # This saves memory by having
            # duplicate strings just point to the same memory.
            token = sys.intern(token.strip(punctuation))

            # Ignore punctuation and stopwords
            if not token or stop_rule(token):
                continue

            tokens.append(token)
        return tokens

    def generate(self):
        """
        Generate some 'speech'.
        """

        tokens = []

        def constraint(tokens):
            return len(' '.join(tokens)) < self.max_chars

        while constraint(tokens):
            next_token = self._next_token()

            # If a token couldn't be found, or
            # if the next token is a stop token,
            # stop.
            if not next_token or next_token == self.stop_token:
                break

            # Update the prev tokens,
            # truncating if necessary.
            self.prev += (next_token,)
            if len(self.prev) > self.n:
                self.prev = self.prev[1:]

            tokens.append(next_token)

        # If the constraint is violated, retry.
        if not constraint(tokens):
            # Not really looking for a good stop candidate,
            # just stop wherever :)
            # Just pop off the last token and call it a day.
            tokens = tokens[:-1]

        # Reset the previous tokens.
        self.prev = ()

        return ' '.join(tokens)

    def _next_token(self):
        """
        Choose the next token.

        If there's a key error, it may be
        because self.prev doesn't have enough grams/tokens in it,
        which  means we're still early in the generation, so just pick
        a random starting token.
        Otherwise, it's probably because the self.prev ngram has never
        been enconutered before. In which case, if self.ramble is True,
        pick a random starting token, otherwise, just end return None.
        """
        try:
            return self._weighted_choice(self.knowledge[self.prev])
        except KeyError:
            if len(self.prev) < self.n or self.ramble:
                return self._weighted_choice(self.knowledge[()])

    def _weighted_choice(self, choices):
        """
        Random selects a key from a dictionary,
        where each key's value is its probability weight.
        """
        # Randomly select a value between 0 and
        # the sum of all the weights.
        rand = random.uniform(0, sum(choices.values()))

        # Seek through the dict until a key is found
        # resulting in the random value.
        summ = 0.0
        for key, value in choices.items():
            summ += value
            if rand < summ: return key
        return key