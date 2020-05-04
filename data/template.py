from abc import ABC, abstractmethod
from typing import List, NamedTuple


class Text(NamedTuple):
    raw: str
    tokenized: List[str]


class Document(NamedTuple):
    id: int
    title: Text
    content: Text
    url: str = ""

    def sections(self):
        return [self.title, self.content]

    def __repr__(self):
        return (f"doc_id: {self.id}\n" +
                f"  title: {self.title.raw}\n" +
                f"  content: {self.content.raw}")


class Query(NamedTuple):
    id: int
    text: Text

    def sections(self):
        return [self.text]

    def __repr__(self):
        return (f"query_id: {self.id}\n" +
                f"  text: {self.text.raw}\n")


class Dataset(ABC):
    def __init__(self):
        self.documents = None
        self.queries = None
        self.relevant_docs = None
        super().__init__()

    @abstractmethod
    def load_docs(self, filename):
        pass

    @abstractmethod
    def load_queries(self, filename):
        pass

    @abstractmethod
    def load_relevant_docs(self, filename):
        pass
