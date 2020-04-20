from abc import ABC, abstractmethod


class Vectorizer(ABC):
    def __init__(self):
        self.vocab = list()
        super().__init__()

    @abstractmethod
    def vectroize_documents(self, documents):
        pass

    @abstractmethod
    def vectroize_query(self, query):
        pass
