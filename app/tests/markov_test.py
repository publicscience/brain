import unittest
from app.brain.markov import Markov

class MarkovTest(unittest.TestCase):
    def setUp(self):
        self.m = Markov()
        self.doc = 'hey this is a test'

    def tearDown(self):
        pass

    def test_tokenizer_default_stop_words(self):
        tokens = self.m.tokenize(self.doc)
        self.assertEqual(tokens, ['hey', 'test'])

    def test_tokenizer_no_stop_words(self):
        tokens = self.m.tokenize(self.doc, stop_words=None)
        self.assertEqual(tokens, ['hey', 'this', 'is', 'a', 'test'])

    def test_tokenizer_custom_stop_words(self):
        tokens = self.m.tokenize(self.doc, stop_words=['is', 'a'])
        self.assertEqual(tokens, ['hey', 'this', 'test'])

    def test_tokenizer_stop_rule(self):
        tokens = self.m.tokenize(self.doc, stop_rule=lambda t: t[0] == 'h')
        self.assertEqual(tokens, ['test'])

    def test_ngramize(self):
        tokens = self.m.tokenize(self.doc, stop_words=None)
        ngrams = [ngram for ngram in self.m.ngramize(tokens)]
        expected = [
            ['<START>', 'hey', 'this', 'is'],
            ['hey', 'this', 'is', 'a'],
            ['this', 'is', 'a', 'test'],
            ['is', 'a', 'test', '<STOP>']
        ]
        self.assertEqual(ngrams, expected)

    def test_train(self):
        expected = {
                ('is', 'a', 'test'): [1, {'<STOP>': 1}],
                ('<START>', 'hey', 'this'): [1, {'is': 1}],
                ('hey', 'this', 'is'): [1, {'a': 1}],
                ('this', 'is', 'a'): [1, {'test': 1}]
        }

        self.m.train([self.doc])
        self.assertEqual(self.m.knowledge, expected)

    def test_train_accumulates(self):
        expected = {
                ('is', 'a', 'test'): [2, {'<STOP>': 2}],
                ('<START>', 'hey', 'this'): [2, {'is': 2}],
                ('hey', 'this', 'is'): [2, {'a': 2}],
                ('this', 'is', 'a'): [2, {'test': 2}]
        }

        self.m.train([self.doc])
        self.m.train([self.doc])
        self.assertEqual(self.m.knowledge, expected)
