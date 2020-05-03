from abc import ABC, abstractmethod


class Vectorizer(ABC):
    def __init__(self):
        super().__init__()
        self.vocab = list()
        self.weighting = ""
        self.weighted_vectorizer = None  # from vectorize.weighting
        self.is_oov_token_allowed = False

    @abstractmethod
    def vectorize_documents(self, documents):
        pass

    @abstractmethod
    def vectorize_query(self, query):
        pass
