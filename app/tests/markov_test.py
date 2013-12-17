import unittest
from app.brain.markov import Markov

class MarkovTest(unittest.TestCase):
    def setUp(self):
        self.m = Markov()
        self.doc = 'hey this is a test?'

    def tearDown(self):
        pass

    def test_tokenizer_default_stop_words(self):
        tokens = self.m.tokenize(self.doc)
        self.assertEqual(tokens, ['hey', 'this', 'is', 'a', 'test'])

    def test_tokenizer_stop_rule(self):
        tokens = self.m.tokenize(self.doc, stop_rule=lambda t: t[0] == 't')
        self.assertEqual(tokens, ['hey', 'is', 'a'])

    def test_ngramize(self):
        tokens = self.m.tokenize(self.doc)
        ngrams = [ngram for ngram in self.m.ngramize(tokens)]
        expected = [
            ['hey', 'this', 'is', 'a'],
            ['this', 'is', 'a', 'test'],
            ['is', 'a', 'test', '<STOP>']
        ]
        self.assertEqual(ngrams, expected)

    def test_train(self):
        # Test ignoring RT and @ mentions.
        tweet =  ' '.join(['RT', self.doc, '@foo'])
        expected = {
                (): {'hey': 1},
                ('is', 'a', 'test'): [1, {'<STOP>': 1}],
                ('hey', 'this', 'is'): [1, {'a': 1}],
                ('this', 'is', 'a'): [1, {'test': 1}]
        }

        self.m.train([tweet])
        self.assertEqual(self.m.knowledge, expected)

    def test_train_accumulates(self):
        expected = {
                (): {'hey': 2},
                ('is', 'a', 'test'): [2, {'<STOP>': 2}],
                ('hey', 'this', 'is'): [2, {'a': 2}],
                ('this', 'is', 'a'): [2, {'test': 2}]
        }

        self.m.train([self.doc])
        self.m.train([self.doc])
        self.assertEqual(self.m.knowledge, expected)

    def test_weighted_choice(self):
        num_trials = 100000
        dict = {
                'A': 25,
                'B': 40,
                'C': 15,
                'D': 20
        }
        results = {}

        for i in range(num_trials):
            choice = self.m._weighted_choice(dict)
            results[choice] = results.get(choice, 0) + 1

        # Convert to percents
        for k, count in results.items():
            results[k] = count/num_trials

        self.assertAlmostEqual(results['A'], 0.25, places=2)
        self.assertAlmostEqual(results['B'], 0.40, places=2)
        self.assertAlmostEqual(results['C'], 0.15, places=2)
        self.assertAlmostEqual(results['D'], 0.20, places=2)

    def test_next_token(self):
        self.m.knowledge = {
                ('why', 'hello', 'there'): {
                    'pal': 1
                }
        }
        self.m.prev = ('why', 'hello', 'there')
        self.assertEqual(self.m._next_token(), 'pal')

    def test_next_token_weighted(self):
        num_trials = 100000
        self.m.knowledge = {
                ('why', 'hello', 'there'): {
                    'pal': 1,
                    'friend': 1
                }
        }
        self.m.prev = ('why', 'hello', 'there')

        results = {}
        for i in range(num_trials):
            token = self.m._next_token()
            results[token] = results.get(token, 0) + 1

        # Convert to percents
        for k, count in results.items():
            results[k] = count/num_trials

        self.assertAlmostEqual(results['pal'], 0.5, places=2)
        self.assertAlmostEqual(results['friend'], 0.5, places=2)

    def test_next_token_insufficient_previous_tokens(self):
        self.m.knowledge = {
                (): {
                    'pal': 1
                }
        }
        self.m.prev = ('why',)
        self.assertEqual(self.m._next_token(), 'pal')

    def test_generate(self):
        self.m.knowledge = {
                (): {
                    'hello': 1
                },
                ('hello', 'hello', 'hello'): {
                    'goodbye': 1
                }
        }
        speech = self.m.generate()
        self.assertEqual(speech,'hello hello hello goodbye')

    def test_generate_under_max_chars(self):
        self.m = Markov(ramble=True)
        self.m.knowledge = {
                (): {
                    'hello': 1
                },
                ('hello', 'hello', 'hello'): {
                    'goodbye': 1
                }
        }
        # Run a few times just to be sure.
        for i in range(1000):
            speech = self.m.generate()
            self.assertLessEqual(len(speech),self.m.max_chars)
