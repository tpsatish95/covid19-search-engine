import random
from abc import ABC, abstractmethod

from gensim.models.keyedvectors import Word2VecKeyedVectors


class Embeddings(ABC):
    def __init__(self, model):
        self.word2vec = model
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        if isinstance(self.word2vec, Word2VecKeyedVectors):
            self.dim = self.word2vec.vectors.shape[1]
        else:
            # or dict() -> {"word": [vec_array]} format
            self.dim = len(self.word2vec.word_vec(random.sample(self.word2vec.vocab, 1)[0]))
        self.is_oov_token_allowed = False

    @abstractmethod
    def fit(self, documents):
        pass

    @abstractmethod
    def transform(self, documents):
        pass
