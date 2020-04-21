from sklearn.metrics.pairwise import cosine_similarity

from data.dummy.loader import dummy_data
from preprocess.processor import TextProcessor
from search_engine import SearchEngine
from vectorize.tf_idf import TfIdfVectorizer


def main():
    text_preprocessor = TextProcessor(remove_stopwords=True,
                                      stemming=True,
                                      replace_urls=False,
                                      strip_white_spaces=True,
                                      re_tokenize=False)
    search_engine = SearchEngine(dataset=dummy_data,
                                 text_preprocessor=text_preprocessor,
                                 vectorizer=TfIdfVectorizer(use_sklearn=True),
                                 similarity_metric=cosine_similarity)
    search_engine.evaluate()

    # print(search_engine.search("computer networks")[0])


if __name__ == '__main__':
    main()
