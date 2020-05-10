import os
import pickle
import re
import string

from nltk.stem.snowball import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction import text

from data.template import Document, Query, Text
from preprocess.spell_check.corrector import spellCheck
from preprocess.twokenize import emoticons, twokenize

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

        self.stemmer = PorterStemmer()
        self.stopwords = set(text.ENGLISH_STOP_WORDS).union(set(string.punctuation))
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

        processed_sections = list()
        for section in object.sections():
            section_tokens = list()
            for word in section.tokenized:
                if self.is_strip_white_spaces:
                    word = word.lower().strip()
                if self.is_remove_stopwords:
                    if word in self.stopwords:
                        continue
                if self.is_replace_acronyms:
                    if word in self.acronyms:
                        word = self.acronyms[word]
                if self.is_expand_contractions:
                    if word in self.contractions:
                        word = self.contractions[word]
                if self.is_substitute_emoticons:
                    if word in self.emoticons:
                        word = emoticons.analyze_tweet_heavy(word)
                if self.is_spelling_autocorrect:
                    if word not in self.words_dict:
                        word = self.spell_check.correct(word)
                for w in word.split():
                    if self.is_stemming:
                        w = self.stemmer.stem(w)
                    section_tokens.append(w)
            processed_sections.append(Text(section.raw, section_tokens))
            if self.is_spelling_autocorrect:
                print(processed_sections)
        object = self._wrap(processed_sections, object)
        object = self.re_tokenize(object)

        return self._wrap(processed_sections, object)

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
