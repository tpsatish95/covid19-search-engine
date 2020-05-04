import warnings
# import argparse
from collections import defaultdict

import numpy as np
from tabulate import tabulate

from data.evaluation.cacm.loader import cacm_data
from data.evaluation.cisi.loader import cisi_data
from data.evaluation.cran.loader import cran_data
from data.evaluation.med.loader import med_data

from preprocess.processor import TextProcessor
from search_engine import SearchEngine
from vectorize.doc2vec import Doc2VecVectorizer
from vectorize.gensim import GensimVectorizer
from vectorize.one_hot import OneHotVectorizer


warnings.filterwarnings("ignore")


def compare_and_evaluate():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--bias", action="store_true")
    # args = parser.parse_args()
    # # python evaluate.py --bias

    datasets = [cacm_data, cisi_data, med_data, cran_data]
    data_idx_to_str = ["cacm", "cisi", "med", "cran"]
    results = list()

    # one-hot encoding (weighting: mean and tf-idf)
    text_preprocessor = TextProcessor(re_tokenize=True,
                                      remove_stopwords=True,
                                      stemming=True)

    for idx, data in enumerate(datasets):
        for weighting_scheme in ["mean", "tf-idf"]:
            print("###########################################")
            print(data_idx_to_str[idx], "one-hot", weighting_scheme)
            search_engine = SearchEngine(dataset=data,
                                         text_preprocessor=text_preprocessor,
                                         vectorizer=OneHotVectorizer(weighting=weighting_scheme),
                                         similarity_metric="cosine")
            results.append([data_idx_to_str[idx], "one-hot", weighting_scheme] +
                           search_engine.evaluate())

    # Word2Vec, GLoVe, and Fasttext encoding (weighting: mean, tf-idf, sif, and usif)
    text_preprocessor = TextProcessor(re_tokenize=True,
                                      remove_stopwords=True,
                                      stemming=False)

    for idx, data in enumerate(datasets):
        for gensim_model in ["word2vec-google-news-300",
                             "glove-twitter-100", "glove-wiki-gigaword-100", "glove-wiki-gigaword-200",
                             "fasttext-wiki-news-subwords-300"]:
            for weighting_scheme in ["mean", "tf-idf", "sif", "usif"]:
                print("###########################################")
                print(data_idx_to_str[idx], gensim_model, weighting_scheme)
                search_engine = SearchEngine(dataset=data,
                                             text_preprocessor=text_preprocessor,
                                             vectorizer=GensimVectorizer(model_name=gensim_model,
                                                                         weighting=weighting_scheme),
                                             similarity_metric="cosine")
                results.append([data_idx_to_str[idx], gensim_model,
                                weighting_scheme] + search_engine.evaluate())

    # Doc2Vec (no weighting_scheme needed)
    text_preprocessor = TextProcessor(re_tokenize=True,
                                      remove_stopwords=True,
                                      stemming=True)

    for idx, data in enumerate(datasets):
        print("###########################################")
        print(data_idx_to_str[idx], "doc2vec", "-")
        search_engine = SearchEngine(dataset=data,
                                     text_preprocessor=text_preprocessor,
                                     vectorizer=Doc2VecVectorizer(),
                                     similarity_metric="cosine")
        results.append([data_idx_to_str[idx], "doc2vec", "-"] + search_engine.evaluate())

    # print results

    header = ["dataset", "embedding", "weighting",
              "p_0.25", "p_0.5", "p_0.75", "p_1.0",
              "p_mean1", "p_mean2", "r_norm", "p_norm"]
    print(tabulate(results, headers=header, tablefmt='orgtbl'))

    # with open('./results.txt', 'w+') as f:
    #     print(tabulate(results, headers=header, tablefmt='orgtbl'), file=f)


def get_best_model():
    print("Top 5 Models Across All Datasets (metric wise):")
    print("###########################################")
    with open("./results.txt", "r") as f:
        lines = f.readlines()
        header, results = lines[0], lines[2:]
        header = [entry.strip() for entry in header.split("|")[1:-1]] + ["f1_score"]
        results = [[entry.strip() for entry in result.split("|")[1:-1]] for result in results]

    permutations_all_data = defaultdict(lambda: defaultdict(list))
    for result in results:
        permutations_all_data[result[1]][result[2]].append([float(x) for x in result[3:]])

    permutations_avg = list()
    for embedding in permutations_all_data:
        for weighting in permutations_all_data[embedding]:
            permutations_avg.append(["("+embedding+", "+weighting+")", [np.mean(metric)
                                                                        for metric in list(zip(*permutations_all_data[embedding][weighting]))]])

    for i in range(9):
        if i == 8:
            def f1_score(x, y): return 2*((x*y)/(x+y))
            top_5_models = sorted(permutations_avg,
                                  key=lambda x: f1_score(x[1][6], x[1][7]),
                                  reverse=True)[:5]
        else:
            top_5_models = sorted(permutations_avg,
                                  key=lambda x: x[1][i],
                                  reverse=True)[:5]

        print("Metric: " + header[3+i])
        print("Top 5 Models (embedding, weighting):")
        for j, t in enumerate(top_5_models):
            print(str(j+1)+". " + t[0])
        print("###########################################")


if __name__ == '__main__':
    compare_and_evaluate()
    get_best_model()
