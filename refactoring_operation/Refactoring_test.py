import unittest
from encoding.IntegerEncoding import IntegerEncoding
from jxplatform2.jClass import jClass
from utils import readJson
from qmood.Qmood import Qmood
import copy
from refactoring_operation.RefactoringOperationDispatcher import dispatch

class MyTestCase(unittest.TestCase):

    def encoding(self):
        repoName = "mbassador"
        jsonFile = "/Users/leichen/Desktop/" + repoName + ".json"
        load = readJson(jsonFile)
        jClist = []
        for each in load:
            jClist.append(jClass(load=each))
        self.projectInfo = jClist
        repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
        self.integerEncoding = IntegerEncoding()

    def test_MoveMethod(self):
        self.encoding()
        decodedIntegerSequences = self.integerEncoding.decoding([2,1,2,1])
        for each in decodedIntegerSequences:
            dispatch(each["ROType"].value)(each, self.projectInfo)

        print(self.projectInfo[0].getClass())
        print([each.name for each in self.projectInfo[0].getMethod()])
        print(self.projectInfo[1].getClass())
        print([each.name for each in self.projectInfo[1].getMethod()])
        self.assertEqual("['handle()', 'afterTest()']",str([each.name for each in self.projectInfo[1].getMethod()]))

    def test_MoveField(self):
        self.encoding()
        projectInfo = copy.deepcopy(self.projectInfo)

        self.integerEncoding.encoding(projectInfo)
        decodedIntegerSequences = self.integerEncoding.decoding([3,1,2,0])

        for each in decodedIntegerSequences:
            dispatch(each["ROType"].value)(each, projectInfo)

        print(self.projectInfo[0].getClass())
        print([each for each in self.projectInfo[0].getField()])
        print(self.projectInfo[1].getClass())
        print([each for each in self.projectInfo[1].getField()])

        self.assertEqual(list(),[each for each in self.projectInfo[1].getField()])
        self.assertEqual("['2#runtime@java.lang.Runtime']",str([each for each in projectInfo[1].getField()]))
        # self.assertEqual("['2#runtime@java.lang.Runtime']",str([each for each in self.projectInfo[1].getField()]))

    def test_RefactoringOperaations(self):
        pass



if __name__ == '__main__':
    unittest.main()
