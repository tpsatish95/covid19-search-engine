import os
import pickle
from collections import defaultdict
from uuid import uuid4

import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import pairwise_distances

from data.template import Query, Text
from performance_metrics import (mean_precision1, mean_precision2,
                                 norm_precision, norm_recall, precision_at)

# from sklearn.decomposition import TruncatedSVD


class SearchEngine(object):
    def __init__(self,
                 dataset,
                 text_preprocessor,
                 vectorizer,
                 similarity_metric):  # can be any parameter from sklearn.metrics.pairwise.pairwise_distances
        self.user_id = str(uuid4())
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

    def load_user_profile(self):
        if os.path.exists('user_profiles.pkl'):
            with open('user_profiles.pkl', 'rb') as f:
                user_profiles = pickle.load(f)
                return user_profiles[self.user_id]
        else:
            return []

    def update_user_profile(self, query):
        user_profiles = defaultdict(list)
        if os.path.exists('user_profiles.pkl'):
            with open('user_profiles.pkl', 'rb') as f:
                user_profiles = pickle.load(f)

        user_profiles[self.user_id].append(query)
        with open('user_profiles.pkl', 'wb') as f:
            pickle.dump(user_profiles, f)

    def personalize_query(self, query_vector, top_n=5):
        user_profile = self.load_user_profile()

        if user_profile:
            profile_vectors = []
            for preference in user_profile:
                preference = self.text_preprocessor.process(Query(uuid4(), Text(preference, [word.lower() for word in word_tokenize(preference)])))
                profile_vectors.append(self.vectorizer.vectorize_query(preference, self.text_preprocessor))
            user_profile_vector = np.mean(profile_vectors, axis=0)

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
            r_av = np.mean(relevant_vectors, axis=0)
            nr_av = np.mean(non_relevant_vectors, axis=0)

            return (a * qO) + (b * r_av) - (g * nr_av)

        return query_vector

    def search(self, query, personalize=False, top_k=25, is_expand_query=False):
        if not isinstance(query, Query):
            query = Query(uuid4(), Text(query, [word.lower() for word in word_tokenize(query)]))

        query = self.text_preprocessor.process(query)
        query_vector = self.vectorizer.vectorize_query(query, self.text_preprocessor, is_expand_query)

        if personalize:
            # perform query personaliziation based on user_profile
            query_vector = self.personalize_query(query_vector)

        # query_vector = self.svd.transform(query_vector)

        results_with_score = 1 - pairwise_distances(query_vector,
                                                    self.document_vectors,
                                                    metric=self.similarity_metric)[0]
        results_with_score = [(doc_id + 1, score)
                              for doc_id, score in enumerate(results_with_score)]
        results_with_score = sorted(results_with_score, key=lambda x: -x[1])
        results = [x[0] for x in results_with_score]

        self.update_user_profile(query.text.raw)

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
