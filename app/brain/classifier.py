import pickle
from os import getcwd, path

from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))

class Classifier():
    """
    Multinomial Naive Bayes classifier.
    Provides binary classification; that is,
    labels are either 0 or 1,
    0 being negative,
    1 being positive.
    """

    def __init__(self, filepath=path.join(__location__, 'classifier.pickle')):
        """
        Initialize the classifier.
        Tries to load the existing one;
        if none exists, a new one is created.
        """
        self.filepath = filepath

        hasher = HashingVectorizer(stop_words='english', non_negative=True, norm=None, binary=False)
        self.vectorizer = Pipeline((
            ('hasher', hasher),
            ('tf_idf', TfidfTransformer())
        ))

        # Try to load the existing classifier.
        self.clf = self.load()

        # If there wasn't one, create a new one.
        if not self.clf:
            self.clf = MultinomialNB(alpha=0.1)

    def train(self, docs, labels, save=True):
        """
        Updates the classifier with new training data.
        By default, saves the updated classifier as well.
        """
        if docs:
            training = self.vectorizer.fit_transform(docs)
            self.clf.partial_fit(training, labels, [0,1])
            if save:
                self.save()

    def classify(self, docs):
        """
        Classifies a list of documents.
        Returns a list of class probabilities
        for each document.
        """
        docs_ = self.vectorizer.fit_transform(docs)
        try:
            return self.clf.predict_proba(docs_)

        # Likely because the classifier hasn't been trained yet.
        except AttributeError:
            return []

    def save(self):
        """
        Persist the classifier to the disk.
        """
        file = open(self.filepath, 'wb')
        pickle.dump(self.clf, file)

    def load(self):
        """
        Load the classifier from disk.
        Returns None if one wasn't found.
        """
        try:
            file = open(self.filepath, 'rb')
            return pickle.load(file)
        except IOError:
            return None
