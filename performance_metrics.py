from typing import List

import numpy as np


def interpolate(x1, y1, x2, y2, x):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m * x + b


def precision_at(recall: float, results: List[int], relevant: List[int]) -> float:
    '''
    This function should compute the precision at the specified recall level.
    If the recall level is in between two points, you should do a linear interpolation
    between the two closest points. For example, if you have 4 results
    (recall 0.25, 0.5, 0.75, and 1.0), and you need to compute recall @ 0.6, then do something like

    interpolate(0.5, prec @ 0.5, 0.75, prec @ 0.75, 0.6)

    Note that there is implicitly a point (recall=0, precision=1).

    `results` is a sorted list of document ids
    `relevant` is a list of relevant documents
    '''
    ranks = list()
    for i, result in enumerate(results):
        if result in relevant:
            ranks.append(i+1)

    recalls = [0]
    precisions = [1]
    for i, rank in enumerate(ranks):
        recalls.append(float(i+1)/float(len(relevant)))
        precisions.append(float(i+1)/float(rank))

    if recall in recalls:
        return precisions[recalls.index(recall)]
    else:
        right_recall_id = np.searchsorted(recalls, recall, side='left', sorter=None)
        left_recall_id = right_recall_id - 1
        return interpolate(recalls[left_recall_id], precisions[left_recall_id],
                           recalls[right_recall_id], precisions[right_recall_id],
                           recall)


def mean_precision1(results, relevant):
    return (precision_at(0.25, results, relevant) +
            precision_at(0.5, results, relevant) +
            precision_at(0.75, results, relevant)) / 3.0


def mean_precision2(results, relevant):
    return sum([precision_at((i+1)/10, results, relevant) for i in range(10)]) / 10.0


def norm_recall(results, relevant):
    Rel = len(relevant)
    N = len(results)

    ranks = list()
    for i, result in enumerate(results):
        if result in relevant:
            ranks.append(i+1)

    rank_sum = sum(ranks)
    i_sum = sum(list(range(1, Rel+1)))

    return 1 - ((rank_sum - i_sum)/(Rel * (N - Rel)))


def norm_precision(results, relevant):
    Rel = len(relevant)
    N = len(results)

    ranks = list()
    for i, result in enumerate(results):
        if result in relevant:
            ranks.append(np.log(i+1))

    rank_sum = sum(ranks)
    i_sum = sum([np.log(i) for i in range(1, Rel+1)])

    return 1 - ((rank_sum - i_sum)/(N*np.log(N) - (N - Rel)*np.log(N - Rel) - Rel*np.log(Rel)))
