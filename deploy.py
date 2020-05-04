import warnings
import argparse

from data.local_news_data.cbs.loader import cbs_covid_data
from data.local_news_data.wbaltv.loader import wbaltv_covid_data

from preprocess.processor import TextProcessor
from search_engine import SearchEngine
from vectorize.gensim import GensimVectorizer
from vectorize.one_hot import OneHotVectorizer

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bias")
    args = parser.parse_args()
    # python evaluate.py --bias

    if args.bias is not None:
        bias_str = args.bias
    else:
        bias_str = ""


    datasets = [cbs_covid_data, wbaltv_covid_data]
    data_idx_to_str = ["cbs", "wbaltv"]


    best_configs = [
        ("one-hot", "tf-idf"),
        ("one-hot", "mean"),
        ("word2vec-google-news-300", "usif"),
        ("word2vec-google-news-300", "sif"),
        ("word2vec-google-news-300", "mean")
        ]

    text_preprocessor = TextProcessor(re_tokenize=True,
                                      remove_stopwords=True,
                                      stemming=True,
                                      replace_acronyms=True,
                                      expand_contractions=True,
                                      spelling_autocorrect=True)

    for idx, data in enumerate(datasets):
        for embedding, weighting_scheme in best_configs:
            print("####################################################")
            print("Model details: ", data_idx_to_str[idx], embedding, weighting_scheme)

            if embedding == "one-hot":
                text_preprocessor.is_stemming = True
                search_engine = SearchEngine(dataset=data,
                                             text_preprocessor=text_preprocessor,
                                             vectorizer=OneHotVectorizer(weighting=weighting_scheme),
                                             similarity_metric="cosine")
            else:
                text_preprocessor.is_stemming = False
                search_engine = SearchEngine(dataset=data,
                                             text_preprocessor=text_preprocessor,
                                             vectorizer=GensimVectorizer(model_name=embedding,
                                                                         weighting=weighting_scheme),
                                             similarity_metric="cosine")

            print("Try the search engine:\n")
            query = input("Query: ")
            print()
            while query != "exit":
                matching_docs = search_engine.search(str(query), bias=bias_str, top_k=5)[0]
                for j, doc in enumerate(matching_docs):
                    print(str(j+1) + ". " + doc.title.raw)
                    print("URL: " + doc.url)
                    print()

                print("####################################################\n")
                query = input("Query: ")


if __name__ == '__main__':
    main()
