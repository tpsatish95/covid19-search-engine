import pyximport; pyximport.install(pyimport=True)

import numpy as np
from sklearn.preprocessing import OneHotEncoder

from vectorize.template import Vectorizer
from vectorize.weighting.mean import MeanEmbeddings
from vectorize.weighting.sif import SIFEmbeddings
from vectorize.weighting.tf_idf import TfidfEmbeddings


class KeyedVectors(object):
    def __init__(self, vocab, vectors):
        self.vocab = set(vocab)
        self.vectors = dict(zip(vocab, vectors))

    def word_vec(self, word):
        return self.vectors[word]


class OneHotVectorizer(Vectorizer):
    def __init__(self, weighting="tf-idf"):
        super().__init__()
        self.weighting = weighting
        self.vocab = None
        self.weighted_vectorizer = None

    def _initalize_model(self, documents):
        vocab = set()
        for document in documents:
            for section in document.sections():
                for word in section.tokenized:
                    vocab.add(word)

        self.vocab = np.array(sorted(list(vocab)))

        onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
        one_hot_vectors = onehot_encoder.fit_transform(self.vocab.reshape(-1, 1))

        model = KeyedVectors(self.vocab, one_hot_vectors)

        if self.weighting == "mean":
            self.weighted_vectorizer = MeanEmbeddings(model)
        elif self.weighting == "tf-idf":
            self.weighted_vectorizer = TfidfEmbeddings(model)
        elif self.weighting == "sif" or self.weighting == "usif":
            self.weighted_vectorizer = SIFEmbeddings(model, self.weighting)

    def vectorize_documents(self, documents):
        self._initalize_model(documents)

        corpus = [[word for section in document.sections() for word in section.tokenized]
                  for document in documents]
        self.weighted_vectorizer.fit(corpus)
        return self.weighted_vectorizer.transform(corpus)

    def vectorize_query(self, query, query_preprocessor, is_expand_query=False):
        query = self.prepare_query(query, query_preprocessor, is_expand_query=is_expand_query)
        return self.weighted_vectorizer.transform(query)
