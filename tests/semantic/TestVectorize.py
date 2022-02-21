import unittest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from semantic.Vectorize import *
from semantic.NameExtractor import NameExtractor
from search_technique.NSGAIIInteger import load_repository

class MyTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.TF_IDF = TF_IDF()
        self.paragraphs = ["Bob has an apple Jane has an apple",
                                        "Biao Biao has a tu zi",
                                        "Bob is being attacked",
                                        "This is an red appple",
                                          "Bob has an apple Biaobiao has a pie"]

    def test_fit_transform(self):
        vectorizer = CountVectorizer()
        res = vectorizer.fit_transform(self.paragraphs)
        print(res[0:1])
        # self.assertEqual(, False)

    def test_cosine_similarities(self):
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(self.paragraphs)
        cosine_similarities = linear_kernel(tfidf[0:1],tfidf).flatten()
        print(cosine_similarities)

    def test_TF_IDF_vectorize(self):
        res = self.TF_IDF.vectorize(self.paragraphs)
        print(res.toarray())
        self.assertEqual(res.shape,(5,16))

    def test_TF_IDF_cosine_similarity_with_paragraphs(self):
        X = self.TF_IDF.vectorize(self.paragraphs)
        res = self.TF_IDF.cosine_similarity(X)
        self.assertEqual(res.tolist(), [0.9999999999999999, 0.12779711260785506, 0.09216795650369576, 0.16028361514592773, 0.6952098330550721])

    def test_TF_IDF_cosine_similarity_with_classes_names(self):
        X = self.TF_IDF.vectorize(["strong concurrent set value next",
                                  'subscription id listeners dispatcher context on subscription '
                                   'subscription by priority desc context dispatcher listeners listener '
                                   'listener message type publication message o existing listener id listeners '
                                   'dispatcher context on subscription subscription by priority desc'])
        res = self.TF_IDF.cosine_similarity(X)
        self.assertEqual(res.tolist(), [1.0000000000000002, 0.0])

    def test_TF_IDF_cosine_similarity_with_example_repo_mbassador(self):
        nameExtractor = NameExtractor()
        jsonFile = "../mbassador.json"
        projectInfo = load_repository(jsonFile=jsonFile, exclude_test=True)
        names_dict = nameExtractor.extract(projectInfo=projectInfo)
        sequence_dict = nameExtractor.dict_names_to_dict_sequence(names_dict)
        X = self.TF_IDF.vectorize(sequence_dict)
        res = self.TF_IDF.cosine_similarity(X)
        print(res)

if __name__ == '__main__':
    unittest.main()
