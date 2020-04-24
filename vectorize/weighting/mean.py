# Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/

import numpy as np

from vectorize.weighting.template import Embeddings


class MeanEmbeddings(Embeddings):
    def __init__(self, model):
        super().__init__(model)

    def fit(self, documents):
        return self

    def transform(self, documents):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in documents
        ])
