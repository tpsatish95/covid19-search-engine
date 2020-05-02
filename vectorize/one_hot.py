import numpy as np
from sklearn.preprocessing import OneHotEncoder

from vectorize.template import Vectorizer
from vectorize.weighting.fast_sentence_embeddings import FSEEmbeddings
from vectorize.weighting.mean import MeanEmbeddings
from vectorize.weighting.tf_idf import TfidfEmbeddings


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
        onehot_encoder.fit(self.vocab.reshape(-1, 1))

        model = dict()
        for word in self.vocab:
            model[word] = onehot_encoder.transform(np.array([word]).reshape(-1, 1)).flatten()

        if self.weighting == "mean":
            self.weighted_vectorizer = MeanEmbeddings(model)
        elif self.weighting == "tf-idf":
            self.weighted_vectorizer = TfidfEmbeddings(model)
        elif self.weighting == "fse":
            self.weighted_vectorizer = FSEEmbeddings(model)

    def vectroize_documents(self, documents):
        self._initalize_model(documents)

        corpus = [[word for section in document.sections() for word in section.tokenized]
                  for document in documents]
        self.weighted_vectorizer.fit(corpus)
        return self.weighted_vectorizer.transform(corpus)

    def vectroize_query(self, query):
        query = [[word for section in query.sections() for word in section.tokenized]]
        return self.weighted_vectorizer.transform(query)
