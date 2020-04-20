from data.dummy.loader import dummy_data
# from data.evaluation.cacm.loader import cacm_data
# from data.evaluation.cisi.loader import cisi_data
from preprocess.processor import TextProcessor
from vectorize.tf_idf import TfIdfVectorizer
from search_engine import SearchEngine
from sklearn.metrics.pairwise import cosine_similarity


def main():
    text_preprocessor = TextProcessor(remove_stopwords=True,
                                      stemming=True,
                                      replace_urls=False,
                                      strip_white_spaces=True,
                                      re_tokenize=False)
    search_engine = SearchEngine(dataset=dummy_data,
                                 text_preprocessor=text_preprocessor,
                                 vectorizer=TfIdfVectorizer(),
                                 similarity_metric=cosine_similarity)
    search_engine.evaluate()

    # print(search_engine.search("computer networks")[0])


if __name__ == '__main__':
    main()
