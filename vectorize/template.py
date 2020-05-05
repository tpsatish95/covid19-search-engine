from abc import ABC, abstractmethod
from copy import deepcopy
from uuid import uuid4

import gensim.downloader as gensim_api

from data.template import Query, Text


class Vectorizer(ABC):
    def __init__(self):
        super().__init__()
        self.vocab = list()
        self.weighting = ""
        self.weighted_vectorizer = None  # from vectorize.weighting
        self.query_token_similarity_model = gensim_api.load("glove-wiki-gigaword-100")

    @abstractmethod
    def vectorize_documents(self, documents):
        pass

    def prepare_query(self, query, query_preprocessor, is_expand_query=False, expand_top_n=3):
        query_tokens = [word for section in query.sections() for word in section.tokenized]
        original_is_stemming = query_preprocessor.is_stemming

        if is_expand_query:
            expanded_query_tokens = deepcopy(query_tokens)

            # as stemming hurts the word2vec model
            query_preprocessor.is_stemming = False
            query = query_preprocessor.process(query)
            query_tokens = [word for section in query.sections() for word in section.tokenized]
            for token in query_tokens:
                if token in self.query_token_similarity_model:
                    similar_tokens = self.query_token_similarity_model.most_similar(token, topn=expand_top_n)
                    # 0.70 is cut off for the similarity score
                    expanded_query_tokens.extend([t[0] for t in similar_tokens if t[1] > 0.70])
            query_preprocessor.is_stemming = original_is_stemming

            # we need to map the new query into the original vocab space, using the same preprocessor
            expanded_query = Query(uuid4(), Text(" ".join(expanded_query_tokens), expanded_query_tokens))
            expanded_query = query_preprocessor.process(expanded_query)
            expanded_query_tokens = [word for section in expanded_query.sections() for word in section.tokenized]

            return [expanded_query_tokens]
        else:
            return [query_tokens]

    @abstractmethod
    def vectorize_query(self, query, query_preprocessor, is_expand_query):
        pass
