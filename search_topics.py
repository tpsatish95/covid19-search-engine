import numpy as np
import scipy.sparse as sparse
from data.local_news_data.cbs.loader import cbs_covid_data
from data.local_news_data.wbaltv.loader import wbaltv_covid_data
from data.template import Dataset

class CovidDataset(Dataset):
    def __init__(self, datasets):
        super().__init__()
        self.documents = list()
        self.load_docs(datasets)

    def load_docs(self, datasets):
        for dataset in datasets:
            self.documents.extend(dataset.documents)

    def load_queries(self, filename):
        pass

    def load_relevant_docs(self, filename):
        pass


def main():
    datasets = [cbs_covid_data, wbaltv_covid_data]
    covid_data = CovidDataset(datasets)
    # import pdb; pdb.set_trace()

    n_nonzero = 0
    vocab = set()
    docnames = []
    for doc in covid_data.documents:
        unique_terms = set(doc.title.raw.strip().split())
        unique_terms |= set(doc.content.raw.strip().split())
        vocab |= unique_terms
        n_nonzero += len(unique_terms)
        docnames.append(doc.id)

    docnames = np.array(docnames)
    vocab = np.array(list(vocab))
    # import pdb; pdb.set_trace()
    
    vocab_sorter = np.argsort(vocab)
    ndocs, nvocab = len(docnames), len(vocab)

    data = np.empty(n_nonzero, dtype=np.intc)
    rows = np.empty(n_nonzero, dtype=np.intc)
    cols = np.empty(n_nonzero, dtype=np.intc)

    ind = 0
    for doc in covid_data.documents:
        docname = doc.id
        terms = doc.title.raw.strip().split() + doc.content.raw.strip().split()
        # import pdb; pdb.set_trace()
        term_indices = vocab_sorter[np.searchsorted(vocab, terms, sorter=vocab_sorter)]

        uniq_indices, counts = np.unique(term_indices, return_counts=True)
        n_vals = len(uniq_indices)
        ind_end = ind + n_vals

        data[ind:ind_end] = counts
        cols[ind:ind_end] = uniq_indices
        doc_idx = np.where(docnames == docname)
        rows[ind:ind_end] = np.repeat(doc_idx, n_vals)

        ind = ind_end

    dtm = sparse.coo_matrix((data, (rows, cols)), shape=(ndocs, nvocab), dtype=np.intc)
    import pdb; pdb.set_trace()





if __name__ == '__main__':
    main()