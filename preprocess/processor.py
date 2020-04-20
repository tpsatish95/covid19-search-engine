import os
import pickle
import re

from nltk.stem.snowball import SnowballStemmer

from data.template import Document, Query, Text
from preprocess.twokenize import emoticons, twokenize
from preprocess.spell_check.corrector import spellCheck

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

        # simple
        self.is_strip_white_spaces = strip_white_spaces
        self.is_remove_stopwords = remove_stopwords
        self.is_stemming = stemming

        # advanced
        self.is_replace_urls = replace_urls
        self.is_re_tokenize = re_tokenize
        self.is_replace_acronyms = replace_acronyms
        self.is_expand_contractions = expand_contractions
        self.is_substitute_emoticons = substitute_emoticons
        self.is_spelling_autocorrect = spelling_autocorrect

        self.stemmer = SnowballStemmer("english")
        self.stopwords = self.load_obj("stopwords_set")
        self.acronyms = self.load_obj("acronyms_dict")
        self.contractions = self.load_obj("contractions_dict")
        self.emoticons = self.load_obj("emoticons_dict")
        self.words_dict = self.load_obj("words_dict")
        self.spell_check = spellCheck()

    def process(self, object):
        if self.is_re_tokenize:
            if self.is_replace_urls:
                object = self.replace_urls(object)
            object = self.re_tokenize(object)
        if self.is_strip_white_spaces:
            object = self.strip_white_spaces(object)
        if self.is_remove_stopwords:
            object = self.strip_white_spaces(object)
        if self.is_replace_acronyms:
            object = self.replace_acronyms(object)
        if self.is_substitute_emoticons:
            object = self.substitute_emoticons(object)
        if self.is_spelling_autocorrect:
            object = self.spelling_autocorrect(object)
        if self.is_stemming:
            object = self.stem(object)

        return object

    def replace_urls(self, object):
        sections = [Text(re.sub(twokenize.Url_RE, " ", section.raw), [])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def re_tokenize(self, object):
        sections = [Text(section.raw, twokenize.tokenize(section.raw))
                    for section in object.sections()]
        return self._wrap(sections, object)

    def strip_white_spaces(self, object):
        sections = [Text(section.raw, [word.lower().strip() for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def remove_stopwords(self, object):
        sections = [Text(section.raw, [word for word in section.tokenized if word not in self.stopwords])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def replace_acronyms(self, object):
        sections = [Text(section.raw, [self.acronyms[word] if word in self.acronyms else word for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def expand_contractions(self, object):
        sections = [Text(section.raw, [self.contractions[word] if word in self.contractions else word for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def substitute_emoticons(self, object):
        sections = [Text(section.raw, [emoticons.analyze_tweet_heavy(word) if word in self.emoticons else word for word in section.tokenized])
                    for section in object.sections()]
        return self._wrap(sections, object)

    def spelling_autocorrect(self, object):
        sections = [Text(section.raw, [self.spell_check.correct(word) if word not in self.words_dict else word for word in section.tokenized])
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
