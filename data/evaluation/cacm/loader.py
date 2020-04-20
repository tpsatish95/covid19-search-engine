# loader.py for cacm

import os
import re
from collections import defaultdict

from nltk.tokenize import word_tokenize

from data.template import Dataset, Document, Query, Text


class CACMDataset(Dataset):
    def __init__(self, base_path):
        self.base_path = base_path
        self.documents = None
        self.queries = None
        self.relevant_docs = None
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
                    # print(i)
                    docs.append(defaultdict(list))
                elif re.match(r'\.\w', line):
                    category = line[1]
                elif line != '':
                    docs[i][category].append(Text(line, [word.lower()
                                                         for word in word_tokenize(line)]))
        # print(docs)
        return docs

    def load_docs(self, filename):
        raw_docs = self.read_raw(filename)
        documents = list()
        for doc_id, _ in enumerate(raw_docs[1:]):
            # print(doc_id)
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
        raw_docs = self.read_raw(filename)
        queries = list()
        for query_id, _ in enumerate(raw_docs[1:]):
            text = None

            raw, tokenized = "", list()
            for entry in raw_docs[query_id+1]["W"]:
                raw += " " + entry.raw
                tokenized.extend(entry.tokenized)
            text = Text(raw, tokenized)

            queries.append(Query(query_id+1, text))

        self.queries = queries

    def load_relevant_docs(self, filename):
        rels = {}
        with open(os.path.join(base_path, filename)) as f:
            for line in f:
                qid, rel = line.strip().split()
                qid = int(qid)
                rel = int(rel)
                if qid not in rels:
                    rels[qid] = []
                rels[qid].append(rel)

        self.relevant_docs = rels


base_path = "./data/evaluation/cacm"
cacm_data = CACMDataset(base_path)
cacm_data.load_docs("cacm.all")
cacm_data.load_queries("query.text")
cacm_data.load_relevant_docs("qrels.text")
