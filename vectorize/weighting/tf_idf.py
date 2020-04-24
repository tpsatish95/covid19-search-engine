# Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/

import random
from collections import defaultdict

import numpy as np
from gensim.models.keyedvectors import Word2VecKeyedVectors
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbeddingVectorizer(object):
    def __init__(self, model):
        self.word2vec = model
        self.word2weight = None
        if isinstance(self.word2vec, Word2VecKeyedVectors):
            self.dim = self.word2vec.vectors.shape[1]
        else:
            # or dict() -> {"word": [vec_array]} format
            self.dim = len(self.word2vec[random.choice(list(self.word2vec.keys()))])

    def fit(self, documents):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(documents)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, documents):
        vectors = list()
        for words in documents:
            vector = np.zeros(self.dim)
            weights_sum = 0.0
            for w in words:
                if w in self.word2vec:
                    tf_idf = (words.count(w) / len(words)) * self.word2weight[w]
                    vector += self.word2vec[w] * tf_idf
                    weights_sum += tf_idf
            if weights_sum:
                vector /= weights_sum
            vectors.append(vector)

        return np.array(vectors)
