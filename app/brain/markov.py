from nltk.tokenize import sent_tokenize
import string, sys, random, pickle
from os import getcwd, path

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))

class Markov():
    def __init__(self, ngram_size=1, max_chars=140, ramble=True, spasm=0.05, filepath=path.join(__location__, 'markov.pickle')):
        """
        ngram_size
        Size of ngrams to use for knowledge. on smaller datasets, a value of 1 is recommended,
        you will get more incoherent blabber, but things won't stop short.
        If you have a large dataset, use a value like 2 or 3. More data at this ngram size means higher quality.

        max_chars
        Maximum characters the generated speech should be under.

        ramble
        Whether or not to randomly pick a next token if the generator gets stuck.

        spasm
        The probability of "spasming", that is, picking a random token as the next token.
        This can make things more interesting!

        filepath
        Where to save/load the Markov to/from.
        """
        self.n = ngram_size
        self.max_chars = max_chars
        self.ramble = ramble
        self.filepath = filepath
        self.spasm = spasm
        self.stop_token = '<STOP>'

        self.knowledge = self.load()

        if self.knowledge is None:
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

    def save(self):
        """
        Saves the knowledge to disk.
        """
        file = open(self.filepath, 'wb')
        pickle.dump(self.knowledge, file)

    def load(self):
        """
        Loads the knowledge from disk.
        """
        try:
            file = open(self.filepath, 'rb')
            return pickle.load(file)
        except IOError:
            return None

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
            for sent in sent_tokenize(doc):
                tokens = self.tokenize(sent, stop_rule=stop_rule)
                if tokens:
                    # Keep track of starting token candidates.
                    start_token = tuple(tokens[0:self.n])
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
                        # prior: {post: count}

                        # Create new prior entry if necessary.
                        if prior not in self.knowledge:
                            self.knowledge[prior] = {}

                        # Create new token entry for this prior
                        # if necessary.
                        if post not in self.knowledge[prior]:
                            self.knowledge[prior][post] = 0

                        # Increment count of this post token
                        # for this prior
                        self.knowledge[prior][post] += 1

        # Save Markov!
        self.save()


    def reset(self):
        """
        Resets the Markov generator's knowledge.
        """
        self.knowledge = {}
        self.knowledge[()] = {}
        self.save()


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
        punctuation = string.punctuation.replace('@', '') + '“”‘’–"'

        for token in doc.split(' '):
            # This saves memory by having
            # duplicate strings just point to the same memory.
            token = sys.intern(token.strip(punctuation))

            # Ignore punctuation and stopwords
            if not token or stop_rule(token):
                continue

            tokens.append(token.lower())
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
            if type(next_token) is tuple:
                self.prev += next_token
                tokens += list(next_token)
            else:
                self.prev += (next_token,)
                tokens.append(next_token)


            if len(self.prev) > self.n:
                self.prev = self.prev[1:]

        # If the constraint is violated, retry.
        if not constraint(tokens):
            full = tokens
            consolidated = self._consolidate(tokens)

            if not consolidated:
                # Just pop off the last token and call it a day.
                tokens = full[:-1]
            else:
                tokens = consolidated

        # Reset the previous tokens.
        self.prev = ()

        return ' '.join(tokens)

    def _consolidate(self, tokens):
        """
        Shortens the generated text so it is
        less than the max character length.

        The strategy is to remove ngrams until
        the list of tokens ends with an ngram that
        has a <STOP> associated with it.
        The truncated list of tokens is returned.
        This list could potentially be empty.
        """
        # The n-length tail of the generated text,
        # to see if it's a stop candidate.
        tail = tuple(tokens[-self.n:])

        # Check if we can stop here.
        # Stop here anyway if tail is (), since it will infinitely recurse,
        # and it implies the tokens list is now empty.
        if not tail or (self.knowledge.get(tail, {}).get('<STOP>', 0) and len(tokens) < self.max_chars):
            return tokens

        # If not, RECURSE!
        else:
            tokens = tokens[0:-self.n]
            return self._consolidate(tokens)

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
        if random.random() < self.spasm:
            return self._weighted_choice(self.knowledge[()])
        else:
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

        # If this returns False,
        # it's likely because the knowledge is empty.
        return False