import unittest
from javamodel.jClass import jClass
import json
from search_technique.SearchROProblemRE import SearchROProblemRE
from search_technique.enviroment.Platform import LocalPlatform

class MyTestCase(unittest.TestCase):
    def test_semantic_coherence(self):
        pass
    def test_tf_idf(self):
        repoName = "javapoet"
        jsonFile = "/Users/leichen/Desktop/StaticalAnalysis/javapoet_two.json"
        with open(jsonFile) as f:
            load = json.load(f)
        jClist = []
        for each in load:
            jClist.append(jClass(load=each))

        platform = LocalPlatform()
        platform.set_repository(repoName)
        s = SearchROProblemRE(jClist, platform)

        X = s.vectorize_classes([jClist[0], jClist[1]])
        cosine_smiliarity = s.calc_cosine_similarity(X).tolist()[1]
        call_relation = s.call_graph.call_relation(jClist[0].getRelativeFilePath(), jClist[1].getRelativeFilePath())
        coherence_socre = 0.2 * cosine_smiliarity + 0.8*call_relation
        print(coherence_socre)


