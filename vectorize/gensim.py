import gensim.downloader as gensim_api
import numpy as np

from vectorize.template import Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class GensimAvgVectorizer(Vectorizer):
    # choose model_name from https://github.com/RaRe-Technologies/gensim-data#models

    def __init__(self, model_name="glove-wiki-gigaword-100"):
        super().__init__()
        self.model = gensim_api.load(model_name)
        self.vocab = self.model.vocab

    def vectroize_documents(self, documents):
        doc_vectors = list()
        for document in documents:
            words = list()
            for section in document.sections():
                for word in section.tokenized:
                    if word in self.vocab:
                        words.append(self.model[word])
            doc_vector = np.average(np.array(words), axis=0)
            doc_vectors.append(doc_vector)

        return np.array(doc_vectors)

    def vectroize_query(self, query):
        words = list()
        for section in query.sections():
            for word in section.tokenized:
                if word in self.vocab:
                    words.append(self.model[word])
        query_vector = np.average(np.array(words), axis=0)
        return query_vector.reshape((1, -1))


class GensimTfIdfVectorizer(Vectorizer):
    # choose model_name from https://github.com/RaRe-Technologies/gensim-data#models

    # Refer: https://medium.com/@ranasinghiitkgp/featurization-of-text-data-bow-tf-idf-avgw2v-tfidf-weighted-w2v-7a6c62e8b097
    def __init__(self, model_name="glove-wiki-gigaword-100"):
        super().__init__()
        self.model = gensim_api.load(model_name)
        self.vocab = self.model.vocab
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 1))
        self.tfidf_dictionary = None

    def vectroize_documents(self, documents):
        # initialize
        corpus = [" ".join([" ".join(section.tokenized)
                  for section in document.sections()]) for document in documents]
        self.tfidf_vectorizer.fit(corpus)
        self.tfidf_dictionary = dict(zip(self.tfidf_vectorizer.get_feature_names(), self.tfidf_vectorizer.idf_))

        doc_vectors = list()
        corpus_lens = [sum([len(section.tokenized)
                       for section in document.sections()]) for document in documents]

        for document, text, text_len in zip(documents, corpus, corpus_lens):
            doc_vector = np.zeros(self.model.vectors.shape[1])
            weights_sum = 0.0
            for section in document.sections():
                for word in section.tokenized:
                    if word in self.vocab and word in self.tfidf_dictionary:
                        gensim_vector = self.model[word]
                        tf_idf = self.tfidf_dictionary[word] * (text.count(word) / text_len)
                        doc_vector += (gensim_vector * tf_idf)
                        weights_sum += tf_idf

            if weights_sum != 0:
                doc_vector /= weights_sum
            doc_vectors.append(doc_vector)

        return np.array(doc_vectors)

    def vectroize_query(self, query):
        search_text = " ".join([" ".join(section.tokenized) for section in query.sections()])
        query_len = sum([len(section.tokenized) for section in query.sections()])

        query_vector = np.zeros(self.model.vectors.shape[1])
        weights_sum = 0.0
        for section in query.sections():
            for word in section.tokenized:
                if word in self.vocab and word in self.tfidf_dictionary:
                    gensim_vector = self.model[word]
                    tf_idf = self.tfidf_dictionary[word] * (search_text.count(word) / query_len)
                    query_vector += (gensim_vector * tf_idf)
                    weights_sum += tf_idf

        if weights_sum != 0:
            query_vector /= weights_sum

        return query_vector.reshape((1, -1))
