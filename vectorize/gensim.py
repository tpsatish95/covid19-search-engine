import gensim.downloader as gensim_api

from vectorize.template import Vectorizer
from vectorize.weighting.fast_sentence_embeddings import FSEEmbeddings
from vectorize.weighting.mean import MeanEmbeddings
from vectorize.weighting.tf_idf import TfidfEmbeddings


class GensimVectorizer(Vectorizer):
    # choose model_name from https://github.com/RaRe-Technologies/gensim-data#models

    def __init__(self, model_name="glove-wiki-gigaword-100", weighting="mean"):
        super().__init__()
        gensim_model = gensim_api.load(model_name)
        if weighting == "mean":
            self.weighted_vectorizer = MeanEmbeddings(gensim_model)
        elif weighting == "tf-idf":
            self.weighted_vectorizer = TfidfEmbeddings(gensim_model)
        elif weighting == "fse":
            self.weighted_vectorizer = FSEEmbeddings(gensim_model)

    def vectroize_documents(self, documents):
        corpus = [[word for section in document.sections() for word in section.tokenized]
                  for document in documents]
        self.weighted_vectorizer.fit(corpus)
        return self.weighted_vectorizer.transform(corpus)

    def vectroize_query(self, query):
        query = [[word for section in query.sections() for word in section.tokenized]]
        return self.weighted_vectorizer.transform(query)
