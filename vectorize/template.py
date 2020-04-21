from abc import ABC, abstractmethod


class Vectorizer(ABC):
    def __init__(self):
        super().__init__()
        self.vocab = list()

    @abstractmethod
    def vectroize_documents(self, documents):
        pass

    @abstractmethod
    def vectroize_query(self, query):
        pass
