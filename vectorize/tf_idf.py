from collections import Counter, defaultdict
from typing import NamedTuple

import numpy as np
from sklearn.feature_extraction.text import \
    TfidfVectorizer as SkLearnTfidfVectorizer

from vectorize.template import Vectorizer


class TermWeights(NamedTuple):
    title: float
    content: float


class TfIdfVectorizer(Vectorizer):
    def __init__(self, region_weigting=TermWeights(title=1, content=1), use_sklearn=False):
        super().__init__()
        self.vocab = list()
        self.num_docs = None
        self.doc_freqs = None
        self.region_weights = region_weigting

        self.use_sklearn = use_sklearn
        self.sklearn_vectorizer = SkLearnTfidfVectorizer(stop_words="english",
                                                         ngram_range=(1, 2))

    def vectroize_documents(self, documents):
        if not self.use_sklearn:
            self.num_docs = len(documents)
            self.doc_freqs = self.compute_document_freqs(documents)
            tfidf_vectors = [self.compute_tfidf(
                document, self.compute_doc_tf(document)) for document in documents]

            doc_vectors = list()
            for tfidf_vector in tfidf_vectors:
                doc_vector = [tfidf_vector[word] if word in tfidf_vector.keys()
                              else 0.0 for word in self.vocab]
                doc_vectors.append(doc_vector)

            return np.array(doc_vectors)
        else:
            corpus = [" ".join([" ".join(section.tokenized)
                                for section in document.sections()]) for document in documents]
            return self.sklearn_vectorizer.fit_transform(corpus)

    def vectroize_query(self, query):
        if not self.use_sklearn:
            tfidf_vector = self.compute_tfidf(query, self.compute_query_tf(query))

            query_vector = [tfidf_vector[word] if word in tfidf_vector.keys()
                            else 0.0 for word in self.vocab]
            return np.array(query_vector).reshape((1, -1))
        else:
            query = [" ".join([" ".join(section.tokenized) for section in query.sections()])]
            return self.sklearn_vectorizer.transform(query)

    def compute_document_freqs(self, documents):
        vocab = set()
        for document in documents:
            for section in document.sections():
                for word in section.tokenized:
                    vocab.add(word)
        self.vocab = sorted(list(vocab))

        doc_freqs = Counter()
        for document in documents:
            words = set()
            for section in document.sections():
                for word in section.tokenized:
                    words.add(word)
            for word in words:
                doc_freqs[word] += 1

        return doc_freqs

    def compute_doc_tf(self, document):
        vec = defaultdict(float)
        for word in document.title.tokenized:
            vec[word] += self.region_weights.title
        for word in document.content.tokenized:
            vec[word] += self.region_weights.content

        return dict(vec)

    def compute_query_tf(self, query):
        vec = defaultdict(float)
        for word in query.text.tokenized:
            vec[word] += self.region_weights.title

        return dict(vec)

    def compute_tfidf(self, document, term_freqs):
        words = set()
        for section in document.sections():
            for word in section.tokenized:
                words.add(word)

        vec = defaultdict(float)
        for word in words:
            if word in self.doc_freqs:
                vec[word] += term_freqs[word] * np.log(self.num_docs/self.doc_freqs[word])
            else:
                vec[word] += 0.0

        return dict(vec)
