import os
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize

from data.template import Dataset, Document, Text


class WBALTVCovidDataset(Dataset):
    def __init__(self, base_path):
        self.base_path = base_path
        self.documents = None
        super().__init__()

    def read_raw(self, filename):
        docs = [defaultdict(list)]  # empty 0 index
        category = ''
        with open(os.path.join(self.base_path, filename)) as f:
            i = 0
            for line in f:
                line = line.strip()
                if line.startswith('.I'):
                    i = int(line[3:])
                    docs.append(defaultdict(list))
                elif re.match(r'\.\w', line):
                    category = line[1]
                elif line != '':
                    docs[i][category].append(Text(line, [word.lower()
                                                         for word in word_tokenize(line)]))
        return docs

    def load_docs(self, filename):
        raw_docs = self.read_raw(filename)
        documents = list()
        for doc_id, _ in enumerate(raw_docs[1:]):
            title, content = None, None

            raw, tokenized = "", list()
            for entry in raw_docs[doc_id+1]["T"]:
                raw += " " + entry.raw
                tokenized.extend(entry.tokenized)
            title = Text(raw, tokenized)

            raw, tokenized = "", list()
            for category in ["A", "K", "W"]:
                for entry in raw_docs[doc_id+1][category]:
                    raw += " " + entry.raw
                    tokenized.extend(entry.tokenized)
            content = Text(raw, tokenized)

            documents.append(Document(doc_id+1, title, content))

        self.documents = documents

    def load_queries(self, filename):
        pass

    def load_relevant_docs(self, filename):
        pass


# load the data
base_path = './data/local_news_data/wbaltv'
wbaltv_covid_data = WBALTVCovidDataset(base_path)
wbaltv_covid_data.load_docs('WBALTV.ALL')
