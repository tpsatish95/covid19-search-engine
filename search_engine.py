from uuid import uuid4

import numpy as np
from nltk.tokenize import word_tokenize

from data.template import Query, Text
from performance_metrics import (mean_precision1, mean_precision2,
                                 norm_precision, norm_recall, precision_at)


class SearchEngine(object):
    def __init__(self,
                 dataset,
                 text_preprocessor,
                 vectorizer,
                 similarity_metric):  # can be function from scipy.spatial.distance
        self.dataset = dataset
        self.text_preprocessor = text_preprocessor
        self.vectorizer = vectorizer
        self.similarity_metric = similarity_metric

        self.document_vectors = None
        self._initialize()

    def _initialize(self):
        documents = [self.text_preprocessor.process(document)
                     for document in self.dataset.documents]
        self.document_vectors = self.vectorizer.vectroize_documents(documents)

    def search(self, query, top_k=25):
        if not isinstance(query, Query):
            query = Query(uuid4(), Text(query, [word.lower() for word in word_tokenize(query)]))

        query = self.text_preprocessor.process(query)
        query_vector = self.vectorizer.vectroize_query(query)

        results_with_score = self.similarity_metric(query_vector, self.document_vectors)[0]
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
