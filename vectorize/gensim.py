import gensim.downloader as gensim_api
import numpy as np

from vectorize.template import Vectorizer


class GensimVectorizer(Vectorizer):
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
