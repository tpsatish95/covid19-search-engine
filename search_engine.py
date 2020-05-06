from uuid import uuid4

import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import pairwise_distances
# from sklearn.decomposition import TruncatedSVD

from data.template import Query, Text
from performance_metrics import (mean_precision1, mean_precision2,
                                 norm_precision, norm_recall, precision_at)


class SearchEngine(object):
    def __init__(self,
                 dataset,
                 text_preprocessor,
                 vectorizer,
                 similarity_metric):  # can be any parameter from sklearn.metrics.pairwise.pairwise_distances
        self.dataset = dataset
        self.text_preprocessor = text_preprocessor
        self.vectorizer = vectorizer
        self.similarity_metric = similarity_metric

        self.document_vectors = None
        # self.svd = TruncatedSVD(n_components=3000, n_iter=10)
        self._initialize()

    def _initialize(self):
        documents = [self.text_preprocessor.process(document)
                     for document in self.dataset.documents]
        self.document_vectors = self.vectorizer.vectorize_documents(documents)
        # self.document_vectors = self.svd.fit_transform(self.document_vectors)

    def personalize_query(self, query_vector, user_profile, top_n=5):
        if not isinstance(user_profile, Query):
            user_profile = Query(uuid4(), Text(user_profile,
                                               [word.lower() for word in word_tokenize(user_profile)]))

        user_profile = self.text_preprocessor.process(user_profile)
        user_profile_vector = self.vectorizer.vectorize_query(user_profile, self.text_preprocessor)

        results_with_score = 1 - pairwise_distances(user_profile_vector,
                                                    self.document_vectors,
                                                    metric=self.similarity_metric)[0]
        results_with_score = [(doc_id + 1, score)
                              for doc_id, score in enumerate(results_with_score)]
        results_with_score = sorted(results_with_score, key=lambda x: -x[1])
        results = [x[0] for x in results_with_score]

        # rocchio feedback
        relevant_vectors = [self.document_vectors[doc_id - 1] for doc_id in results[:top_n]]
        non_relevant_vectors = [self.document_vectors[doc_id - 1] for doc_id in results[-top_n:]]

        a, b, g = 1.0, 0.9, 0.1
        qO = query_vector
        r_av = np.mean(np.array(relevant_vectors), axis=0)
        nr_av = np.mean(np.array(non_relevant_vectors), axis=0)

        return (a * qO) + (b * r_av) - (g * nr_av)

    def search(self, query, user_profile="", top_k=25, is_expand_query=False):
        if not isinstance(query, Query):
            query = Query(uuid4(), Text(query, [word.lower() for word in word_tokenize(query)]))

        query = self.text_preprocessor.process(query)
        query_vector = self.vectorizer.vectorize_query(query, self.text_preprocessor, is_expand_query)

        if user_profile:
            # perform query personaliziation based on user_profile
            query_vector = self.personalize_query(query_vector, user_profile)

        # query_vector = self.svd.transform(query_vector)

        results_with_score = 1 - pairwise_distances(query_vector,
                                                    self.document_vectors,
                                                    metric=self.similarity_metric)[0]
        results_with_score = [(doc_id + 1, score)
                              for doc_id, score in enumerate(results_with_score)]
        results_with_score = sorted(results_with_score, key=lambda x: -x[1])
        results = [x[0] for x in results_with_score]

        return [self.dataset.documents[doc_id - 1] for doc_id in results][:top_k], results

    def evaluate(self):
        metrics = []
        for query in self.dataset.queries:
            _, results = self.search(query)
            relevant = self.dataset.relevant_docs[query.id]

            metrics.append([
                precision_at(0.25, results, relevant),
                precision_at(0.5, results, relevant),
                precision_at(0.75, results, relevant),
                precision_at(1.0, results, relevant),
                mean_precision1(results, relevant),
                mean_precision2(results, relevant),
                norm_recall(results, relevant),
                norm_precision(results, relevant)
            ])

        averages = [f'{np.mean([metric[i] for metric in metrics]):.4f}'
                    for i in range(len(metrics[0]))]
        print("p_0.25: {}, p_0.5: {}, p_0.75: {}, p_1.0: {}, p_mean1: {}, p_mean2: {}, r_norm: {}, p_norm: {}".format(*averages))

        return averages
