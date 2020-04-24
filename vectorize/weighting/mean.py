# Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/

import random

import numpy as np
from gensim.models.keyedvectors import Word2VecKeyedVectors


class MeanEmbeddingVectorizer(object):
    def __init__(self, model):
        self.word2vec = model
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        if isinstance(self.word2vec, Word2VecKeyedVectors):
            self.dim = self.word2vec.vectors.shape[1]
        else:
            # or dict() -> {"word": [vec_array]} format
            self.dim = len(self.word2vec[random.choice(list(self.word2vec.keys()))])

    def fit(self, documents):
        return self

    def transform(self, documents):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in documents
        ])
