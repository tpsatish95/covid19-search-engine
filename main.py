from data.dummy.loader import dummy_data
from preprocess.processor import TextProcessor
from vectorize.tf_idf import TfIdfVectorizer


def main():
    text_preprocessor = TextProcessor(remove_stopwords=True,
                                      stemming=True,
                                      replace_urls=False,
                                      strip_white_spaces=True,
                                      re_tokenize=False)
    documents = [text_preprocessor.process(document) for document in dummy_data.documents]
    queries = [text_preprocessor.process(query) for query in dummy_data.queries]

    vectorizer = TfIdfVectorizer()
    document_vectors = vectorizer.vectroize_documents(documents)
    for query in queries[1:]:
        query_vector = vectorizer.vectroize_query(query)

        # test
        print(sum(document_vectors[1]))
        print(sum(query_vector[0]))
        break


if __name__ == '__main__':
    main()
