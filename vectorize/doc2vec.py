import pyximport; pyximport.install(pyimport=True)

import numpy as np
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from vectorize.template import Vectorizer


class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''

    def __init__(self):
        self.epoch = 1

    def on_epoch_begin(self, model):
        print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        print("Epoch #{} done".format(self.epoch))
        self.epoch += 1


class Doc2VecVectorizer(Vectorizer):
    def __init__(self, is_expand_query=False):
        super().__init__(is_expand_query)
        self.vectroizer = None

    def _initalize_model(self, corpus):
        corpus = [TaggedDocument(document, [i]) for i, document in enumerate(corpus)]

        callbacks = []
        # callbacks = [EpochLogger()]

        self.vectroizer = Doc2Vec(vector_size=100, min_count=2, epochs=50, callbacks=callbacks)
        self.vectroizer.build_vocab(corpus)
        self.vectroizer.train(corpus, total_examples=self.vectroizer.corpus_count,
                              epochs=self.vectroizer.epochs)

    def vectorize_documents(self, documents):
        corpus = [[word for section in document.sections() for word in section.tokenized]
                  for i, document in enumerate(documents)]
        self._initalize_model(corpus)
        return np.array([self.vectroizer.infer_vector(document) for document in corpus])

    def vectorize_query(self, query, query_preprocessor):
        query = self.prepare_query(query, query_preprocessor)[0]
        return np.array([self.vectroizer.infer_vector(query)])
