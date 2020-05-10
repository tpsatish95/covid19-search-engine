# Smooth Inverse Frequency (https://openreview.net/forum?id=SyK00v5xx)
# Refer: https://github.com/oborchers/Fast_Sentence_Embeddings
# Refer: https://towardsdatascience.com/fse-2b1ffa791cf9
import pyximport; pyximport.install(pyimport=True)

from fse import IndexedList
from fse.models import SIF, uSIF

from vectorize.weighting.template import Embeddings


class SIFEmbeddings(Embeddings):
    def __init__(self, model, sif_type):
        super().__init__(model)
        self.fse_indexed_documents = None
        if sif_type == "usif":
            self.sif_model = uSIF(self.word2vec, workers=2, lang_freq="en")
        else:
            self.sif_model = SIF(self.word2vec, workers=2, lang_freq="en")

    def fit(self, documents):
        self.fse_indexed_documents = IndexedList(documents)
        self.sif_model.train(self.fse_indexed_documents)
        return self

    def transform(self, documents):
        documents = IndexedList(documents)
        return self.sif_model.infer(documents)
