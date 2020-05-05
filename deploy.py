import argparse
import warnings

from data.local_news_data.cbs.loader import cbs_covid_data
from data.local_news_data.wbaltv.loader import wbaltv_covid_data
from data.template import Dataset

from preprocess.processor import TextProcessor
from search_engine import SearchEngine
from vectorize.gensim import GensimVectorizer
from vectorize.one_hot import OneHotVectorizer

warnings.filterwarnings("ignore")


class CovidDataset(Dataset):
    def __init__(self, datasets):
        super().__init__()
        self.documents = list()
        self.load_docs(datasets)

    def load_docs(self, datasets):
        for dataset in datasets:
            self.documents.extend(dataset.documents)

    def load_queries(self, filename):
        pass

    def load_relevant_docs(self, filename):
        pass


def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_profile", default="")
    return parser.parse_args()


def main():
    args = arguments_parser()

    datasets = [cbs_covid_data, wbaltv_covid_data]
    covid_data = CovidDataset(datasets)

    # (embedding, weighting_scheme)
    best_configs = [
        ("one-hot", "tf-idf"),  # 1
        # ("one-hot", "mean"),  # 2
        ("word2vec-google-news-300", "usif"),  # 3
        # ("word2vec-google-news-300", "sif"),  # 4
        # ("word2vec-google-news-300", "mean")  # 5
    ]

    for embedding, weighting_scheme in best_configs:
        print("####################################################")
        print("Model details: ", embedding, weighting_scheme)

        text_preprocessor = TextProcessor(re_tokenize=True,
                                          remove_stopwords=True,
                                          stemming=True,
                                          expand_contractions=True,
                                          replace_acronyms=True,
                                          substitute_emoticons=True)

        if embedding == "one-hot":
            text_preprocessor.is_stemming = True
            search_engine = SearchEngine(dataset=covid_data,
                                         text_preprocessor=text_preprocessor,
                                         vectorizer=OneHotVectorizer(weighting=weighting_scheme),
                                         similarity_metric="cosine")
        else:
            text_preprocessor.is_stemming = False
            search_engine = SearchEngine(dataset=covid_data,
                                         text_preprocessor=text_preprocessor,
                                         vectorizer=GensimVectorizer(model_name=embedding,
                                                                     weighting=weighting_scheme),
                                         similarity_metric="cosine")

        # for query processing (mispelled query text)
        # Note: due to long search engine deploy time reasons,
        #       we are not performing spell check on the documents
        search_engine.text_preprocessor.is_spelling_autocorrect = True

        print("Search engine initialized! Try the search engine:\n")
        query = input("Query: ")
        print()

        while query != "exit":
            matching_docs = search_engine.search(str(query),
                                                 user_profile=args.user_profile,
                                                 top_k=5)[0]

            for j, doc in enumerate(matching_docs):
                print(str(j+1) + ". " + doc.title.raw)
                print("URL: " + doc.url)
                print()

            print("####################################################\n")
            query = input("Query: ")


if __name__ == '__main__':
    main()
