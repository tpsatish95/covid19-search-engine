from collections import defaultdict

import gensim.downloader as gensim_api
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from vectorize.template import Vectorizer


class GensimTfIdfVectorizer(Vectorizer):
    # choose model_name from https://github.com/RaRe-Technologies/gensim-data#models

    # Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
    def __init__(self, model_name="glove-wiki-gigaword-100"):
        super().__init__()
        self.model_name = model_name
        self.tf_idf_embedding_vectorizer = None

    def vectroize_documents(self, documents):
        corpus = [[word for section in document.sections() for word in section.tokenized] for document in documents]
        self.tf_idf_embedding_vectorizer = TfidfEmbeddingVectorizer(self.model_name)
        self.tf_idf_embedding_vectorizer.fit(corpus)
        return self.tf_idf_embedding_vectorizer.transform(corpus)

    def vectroize_query(self, query):
        query = [[word for section in query.sections() for word in section.tokenized]]
        return self.tf_idf_embedding_vectorizer.transform(query)


class TfidfEmbeddingVectorizer(object):
    def __init__(self, model_name):
        self.word2vec = gensim_api.load(model_name)
        self.word2weight = None
        self.dim = self.word2vec.vectors.shape[1]

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
