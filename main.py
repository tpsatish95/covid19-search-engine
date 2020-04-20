from data.dummy.loader import dummy_data
from preprocess.processor import TextProcessor


def main():
    print(dummy_data.documents[1])
    text_preprocess = TextProcessor(*[True]*9)
    print(text_preprocess.process(dummy_data.documents[1]).sections())
    print(text_preprocess.process(dummy_data.queries[1]).sections())


if __name__ == '__main__':
    main()
