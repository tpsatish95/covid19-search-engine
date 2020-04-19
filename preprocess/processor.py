import os
import pickle

from nltk.stem.snowball import SnowballStemmer

from data.template import Document, Query, Text

models_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")


class TextProcessor:
    def __init__(self,
                 remove_stopwords=False,
                 stemming=False,
                 replace_acronyms=False,
                 substitute_emoticons=False,
                 expand_contractions=False,
                 spelling_autocorrect=False,
                 replace_urls=True,
                 strip_white_spaces=True,
                 re_tokenize=True):

        self.is_strip_white_spaces = strip_white_spaces
        self.is_remove_stopwords = remove_stopwords
        self.is_stemming = stemming
        self.is_spelling_autocorrect = spelling_autocorrect

        self.is_re_tokenize = re_tokenize
        self.is_replace_urls = replace_urls
        self.is_replace_acronyms = replace_acronyms
        self.is_substitute_emoticons = substitute_emoticons
        self.is_expand_contractions = expand_contractions

        self.stemmer = SnowballStemmer("english")
        self.stopwords = self.load_obj("stopwords_set")

    def process(self, object):
        if self.is_re_tokenize:
            pass

        if self.is_strip_white_spaces:
            object = self.strip_white_spaces(object)
        if self.is_remove_stopwords:
            object = self.strip_white_spaces(object)
        if self.is_stemming:
            object = self.stem(object)

    def strip_white_spaces(self, object):
        sections = [Text(section.raw, [word.strip() for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def remove_stopwords(self, object):
        sections = [Text(section.raw, [word for word in section.tokenized if word not in self.stopwords])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def stem(self, object):
        sections = [Text(section.raw, [self.stemmer.stem(word) for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def _wrap(self, sections, object):
        if isinstance(object, Document):
            return Document(object.id, *sections)
        elif isinstance(object, Query):
            return Query(object.id, *sections)

    def load_obj(self, name):
        with open(os.path.join(models_path, name + '.pkl'), 'rb') as f:
            return pickle.load(f)
