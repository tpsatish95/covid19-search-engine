# Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
# Refer: https://towardsdatascience.com/supercharging-word-vectors-be80ee5513d
import pyximport; pyximport.install(pyimport=True)

from collections import defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from vectorize.weighting.template import Embeddings


class TfidfEmbeddings(Embeddings):
    def __init__(self, model):
        super().__init__(model)
        self.word2weight = None

    def fit(self, documents):
        tfidf = TfidfVectorizer(ngram_range=(1, 2), analyzer=lambda x: x)
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
        processed_documents = list()
        for words in documents:
            n = len(words)
            sentence_vector = np.zeros(self.dim)
            for w in words:
                if (self.is_oov_token_allowed or w in self.word2vec.vocab):
                    sentence_vector += (self.word2vec.word_vec(w) * self.word2weight[w])
            if n:
                sentence_vector /= n
            processed_documents.append(sentence_vector)

        return np.array(processed_documents)
