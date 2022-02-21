from abc import abstractmethod,ABC
from typing import Generic,List,TypeVar
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
S = TypeVar("S")

class Vectorize(ABC):
    """
    class vectorize words
    """
    @abstractmethod
    def vectorize(self, paragraphs:List[str]):
        """ vectorize word list"""

    @abstractmethod
    def cosine_similarity(self, document_term_matrix):
        """Calculate the cosine_similarity between document_term_matrix"""

class TF_IDF(Vectorize):
    "use TF IDF to vectorize code elements"
    def vectorize(self, paragraphs:List[str]):
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(paragraphs)
        return X

    def cosine_similarity(self, document_term_matrix):
        "input should be a document_term_matrix with 2 rows (names in 2 classes)"
        cosine_similarities = linear_kernel(document_term_matrix[0:1], document_term_matrix).flatten()
        return cosine_similarities

class Word2vec(Vectorize):
    "use word2vec to vectorize code elements"
    def vectorize(self) ->List:
        pass

