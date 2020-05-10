# Refer: http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/

import numpy as np

from vectorize.weighting.template import Embeddings


class MeanEmbeddings(Embeddings):
    def __init__(self, model):
        super().__init__(model)

    def fit(self, documents):
        return self

    def transform(self, documents):
        processed_documents = list()
        for words in documents:
            n = len(words)
            sentence_vector = np.zeros(self.dim)
            for w in words:
                if (self.is_oov_token_allowed or w in self.word2vec.vocab):
                    sentence_vector += self.word2vec.word_vec(w)
            if n:
                sentence_vector /= n
            processed_documents.append(sentence_vector)

        return np.array(processed_documents)
