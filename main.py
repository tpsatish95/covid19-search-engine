import warnings

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

    # TODO: Fix fasttext for OOV tokens
    # TODO: BERT and ELMo encoding (weighting: mean, ttf-idf, sif, and usif)
    # TODO: Try Baltimore Sun and WBALTV, print(search_engine.search("<custom-text>")[0])
    # TODO: Sentence level embeddings

    # print results
    with open('./results.txt', 'w+') as f:
        header = ["dataset", "embedding", "weighting",
                  "p_0.25", "p_0.5", "p_0.75", "p_1.0",
                  "p_mean1", "p_mean2", "r_norm", "p_norm"]
        print(tabulate(results, headers=header, tablefmt='orgtbl'))
        print(tabulate(results, headers=header, tablefmt='orgtbl'), file=f)


if __name__ == '__main__':
    compare_and_evaluate()
