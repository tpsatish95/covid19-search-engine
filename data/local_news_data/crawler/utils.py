# -*- coding: utf-8 -*-
"""
This file contains helper methods using during web crawling, processing
jsonl output into csv format, and processing csv format into document
format required by Dataset loader.

Some methods adopted from RISJbot (https://github.com/pmyteh/RISJbot)
"""
import logging
import os
import re

import jsonlines
import lxml.etree
import pandas as pd
from cssselect import HTMLTranslator

logger = logging.getLogger(__name__)

KEYWORDS = ['covid', 'coravirus', 'resources', 'covid-19', 'store', 'essential', 'relief',
            'covid 19', 'food', 'grocery', 'groceries', 'help', 'quarantine', 'restaurants']
TEXT_WORDS = ['covid', 'coravirus', 'covid-19', 'covid 19',
              'grocery store', 'quarantine', 'social distance']


def process_jsonl(*, filename):
    """
    Helper function to parse information from jsonl

    @arg filename - name of jsonl file
    @return dataframe with information to be saved to CSV
    """
    df = pd.DataFrame(columns=['url', 'keywords', 'headline', 'author', 'source', 'summary', 'bodytext',
                               'sentiment', 'subjectivity', 'wordcount', 'fetchtime', 'firstpubtime', 'modtime'])
    with jsonlines.open(filename) as reader:
        keywords = []
        for i, obj in enumerate(reader):
            if 'bodytext' not in obj:
                continue
            if 'bodytext' in obj and len(obj['bodytext'].strip().split()[0]) > 30:
                continue
            body = obj['bodytext'].split('—              ')[0].strip()
            if 'keywords' in obj:  # for collecting all keywords in crawled data
                keywords.extend(obj['keywords'])
            if 'keywords' in obj and any(k in obj['keywords'] for k in KEYWORDS):
                df.loc[i] = [obj['url'], ','.join(obj['keywords']), obj['headline'].strip(), obj['bylines'], obj['source'],
                             obj['summary'], body, obj['sentiment'], obj['subjectivity'],
                             obj['wordcount'], obj['fetchtime'], obj['firstpubtime'], obj['modtime']]
            elif 'bodytext' in obj and any(k in obj['bodytext'].lower() for k in TEXT_WORDS):
                df.loc[i] = [obj['url'], '', obj['headline'].strip(), '', '',
                             '', body, obj['sentiment'], obj['subjectivity'],
                             obj['wordcount'], obj['fetchtime'], '', obj['modtime']]
                if 'bylines' in obj:
                    df.loc[i, 'author'] = ' '.join(obj['bylines'])
                if 'source' in obj:
                    df.loc[i, 'source'] = obj['source']
                if 'summary' in obj:
                    df.loc[i, 'summary'] = obj['summary']
                if 'firstpubtime' in obj:
                    df.loc[i, 'firstpubtime'] = obj['firstpubtime']
    return df


def clean_raw(*, path, filename, new_filename):
    """
    Script to format CSV data into .I .T .W
    """
    df = pd.read_csv(os.path.join(path, filename))
    with open(os.path.join(path, new_filename), 'w') as f:
        for i, row in df.iterrows():
            f.write('.I {}\n'.format(i + 1))
            f.write('.U\n{}\n'.format(row.url))
            if len(row.headline) > 0:
                f.write('.T\n{}\n'.format(row.headline))
            f.write('.W\n{}\n\n{}\n'.format(row.summary, row.bodytext))


def clean_search_crawl(*, path, filename, new_filename):
    """
    Script to format CSV data into .I .T .W
    """
    df = pd.read_csv(os.path.join(path, filename))
    with open(os.path.join(path, new_filename), 'w') as f:
        for i, row in df.iterrows():
            f.write('.I {}\n'.format(i + 1))
            f.write('.U\n{}\n'.format(row.url))
            if len(row.title) > 0:
                f.write('.T\n{}\n'.format(row.title))
            f.write('.W\n{}\n'.format(row.body))



def mutate_selector_del(selector, method, expression):
    """Under the covers, Selectors contain an lxml.etree.Element document
       root, which is not exposed by the Selector interface. This is mutatable
       using the .remove method on parts of the selector.root document tree.
       Unfortunately, there is no native content removal interface in scrapy.

       As this is not using a published interface for Selector, it must be
       considered risky. In particular, it is feasible (though not likely) that
       scrapy could change its selector implementation to use a different
       HTML/XML parsing library, at which point this would fail.
    """
    try:
        if method == 'xpath':
            s = expression
        elif method == 'css':
            s = HTMLTranslator().css_to_xpath(expression)
        else:
            raise NotImplementedError

        for node in selector.root.xpath(s):
            node.getparent().remove(node)
    except Exception as e:
        logger.error('mutate_selector_del({}, {}, {},) failed: {}'.format(
            selector,
            method,
            expression,
            e))


def mutate_selector_del_xpath(selector, xpath_str):
    mutate_selector_del(selector, 'xpath', xpath_str)


def mutate_selector_del_css(selector, css_str):
    mutate_selector_del(selector, 'css', css_str)


def split_multiple_byline_string(s):
    for y in s.split(' and '):
        for tok in y.split(','):
            if re.search(r'(correspondent|reporter)', tok, flags=re.IGNORECASE):
                continue
            else:
                yield tok


class NewsSitemap(object):
    """Class to parse Sitemap (type=urlset) and Sitemap Index
    (type=sitemapindex) files. Adapted from scrapy.utils.sitemap."""

    def __init__(self, xmltext):
        xmlp = lxml.etree.XMLParser(recover=True,
                                    remove_comments=True,
                                    resolve_entities=False)
        self._root = lxml.etree.fromstring(xmltext, parser=xmlp)
        rt = self._root.tag
        self.type = self._root.tag.split('}', 1)[1] if '}' in rt else rt

    def __iter__(self):
        for elem in self._root.getchildren():
            d = etree_to_recursive_dict(elem)[1]

            if 'loc' in d:
                yield d


def etree_to_recursive_dict(element):
    # Note: eliminates namespaces, like the original Sitemap
    tag = element.tag
    name = tag.split('}', 1)[1] if '}' in tag else tag

    txt = None
    if element.text:
        txt = element.text.strip()

    # Slightly less flexible than the standard implementation, in that
    # multiple alternates with the same language code (or None) will
    # clobber each other. Also needs support in the parsing code (different
    # interface).
    if name == 'link':
        if 'href' in element.attrib:
            return 'alternate{}'.format(element.get('hreflang')), \
                element.get('href')
    return name, dict(map(etree_to_recursive_dict, element)) or txt
