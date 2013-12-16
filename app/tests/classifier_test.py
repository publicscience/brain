import unittest, os
from app.brain.classifier import Classifier

pos_docs = [
        'dog bar',
        'foo dog',
        'foo bar'
]
neg_docs = [
        'cat har',
        'boo cat',
        'boo har'
]
new_docs = [
        'dog pig',
        'foo pig',
        'bar pig'
]

docs = pos_docs + neg_docs
labels = [1 for i in range(len(pos_docs))] + [0 for i in range(len(neg_docs))]

test_filepath = 'app/tests/classifier.pickle'

class ClassifierTest(unittest.TestCase):
    def setUp(self):
        self.clf = Classifier(filepath=test_filepath)

    def tearDown(self):
        # Clean up test pickle.
        try:
            os.remove(test_filepath)
        except FileNotFoundError:
            pass

    def test_train(self):
        self.clf.train(docs, labels, save=False)
        self.assertEqual(list(self.clf.clf.class_count_), [3.0, 3.0])

    def test_online_train(self):
        self.clf.train(docs, labels, save=False)
        self.clf.train(new_docs, [1,1,1], save=False)
        self.assertEqual(list(self.clf.clf.class_count_), [3.0, 6.0])

    def test_classify(self):
        self.clf.train(docs, labels, save=False)
        probs = self.clf.classify(['foo dog bar'])[0]
        self.assertEqual(1, round(probs[1]))

    def test_save_and_load(self):
        self.clf.train(docs, labels, save=True)
        clf = self.clf.load()
        self.assertEqual(list(clf.class_count_), [3.0, 3.0])

if __name__ == '__main__':
    unittest.main()
