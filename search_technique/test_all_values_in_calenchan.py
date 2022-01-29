from encoding.IntegerEncoding import IntegerEncoding
from jxplatform2.jClass import jClass
from utils import readJson
from qmood.Qmood import Qmood
import copy
from refactoring_operation.RefactoringOperationDispatcher import dispatch

class Test_all_values:
    def __init__(self,projectInfo,repoPath):
        self.projectInfo = projectInfo
        self.repoPath = repoPath
        self.number_of_refactorings = 1
        self.integerEncoding = IntegerEncoding()
        self.integerEncoding.encoding(self.projectInfo)
        self.lower_bound = [1, 1, 1, 1] * self.number_of_refactorings
        self.upper_bound = [self.integerEncoding.ROTypeNum,
                            self.integerEncoding.classNum,
                            self.integerEncoding.classNum,
                            self.integerEncoding.N] * self.number_of_refactorings
        self.initial_objectives = Qmood().calculateQmood(self.projectInfo)


    def test(self):
        for i1 in range(self.lower_bound[0]+1,self.upper_bound[0]):
            for i2 in range(self.lower_bound[1],self.upper_bound[1]):
                for i3 in range(self.lower_bound[1], self.upper_bound[1]):
                    for i4 in range(self.lower_bound[1], self.upper_bound[1]):
                            projectInfo = copy.deepcopy(self.projectInfo)
                            decodedIntegerSequences = self.integerEncoding.decoding([i1,i2,i3,i4])
                            for each in decodedIntegerSequences:
                                dispatch(each["ROType"].value)(each, projectInfo)
                            'calculate QMOOD  after executed refactoring operations'
                            qmood_metrics_value = Qmood().calculateQmood(projectInfo)
                            qmood_metrics_list = ["Effectiveness", "Extendibility", "Flexibility", "Functionality",
                                                  "Resusability",
                                                  "Understandability"]
                            with open("/Users/leichen/Desktop/outputmbassador/results.txt","w") as f:
                                f.write(str([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in
                                   qmood_metrics_list]))
                            print([(qmood_metrics_value[metric] - self.initial_objectives[metric]) for metric in
                                   qmood_metrics_list])


if __name__ =="__main__":
    repoName = "mbassador"
    jsonFile = "/Users/leichen/Desktop/" +repoName +".json"
    load = readJson(jsonFile)
    jClist = []
    for each in load:
        jClist.append(jClass(load=each))
    projectInfo =jClist
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
    testentity = Test_all_values(projectInfo,repoPath)
    testentity.test()
    # print(testentity.upper_bound)
