from data.evaluation.cacm.loader import cacm_data
from data.evaluation.cisi.loader import cisi_data
from data.evaluation.cran.loader import cran_data
from data.evaluation.med.loader import med_data

from preprocess.processor import TextProcessor
from search_engine import SearchEngine
from vectorize.doc2vec import Doc2VecVectorizer


def main():
    text_preprocessor = TextProcessor(re_tokenize=True,
                                      remove_stopwords=True,
                                      stemming=True)

    for data in [cacm_data, cisi_data, med_data, cran_data]:
        search_engine = SearchEngine(dataset=data,
                                     text_preprocessor=text_preprocessor,
                                     vectorizer=Doc2VecVectorizer(),
                                     similarity_metric="cosine")
        search_engine.evaluate()

        # print(search_engine.search("<custom-text>")[0])


if __name__ == '__main__':
    main()
