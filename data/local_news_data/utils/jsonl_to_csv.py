import jsonlines
import os
import pandas as pd

KEYWORDS = ['covid', 'coravirus', 'resources', 'covid-19', 'store', 'essential', 'relief',
            'covid 19', 'food', 'grocery', 'groceries', 'help', 'quarantine', 'restaurants']
TEXT_WORDS = ['covid', 'coravirus', 'covid-19', 'covid 19',
              'grocery store', 'quarantine', 'social distance']


def process_jsonl(filename):
    df = pd.DataFrame(columns=['url', 'keywords', 'headline', 'author', 'source', 'summary', 'bodytext',
                               'sentiment', 'subjectivity', 'wordcount', 'fetchtime', 'firstpubtime', 'modtime'])
    with jsonlines.open(filename) as reader:
        keywords = []
        for i, obj in enumerate(reader):
            # import pdb; pdb.set_trace()
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
                # import pdb; pdb.set_trace()
                if 'bylines' in obj:
                    df.loc[i, 'author'] = ' '.join(obj['bylines'])
                if 'source' in obj:
                    df.loc[i, 'source'] = obj['source']
                if 'summary' in obj:
                    df.loc[i, 'summary'] = obj['summary']
                if 'firstpubtime' in obj:
                    df.loc[i, 'firstpubtime'] = obj['firstpubtime']
    return df
    