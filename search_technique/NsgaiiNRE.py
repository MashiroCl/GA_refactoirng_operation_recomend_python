import sys
sys.path.append("../")
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import WriteFrontToFileObserver, BasicObserver
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService
from search_technique.SearchROProblemNRE import SearchROProblemNRE
from call_graph.CallGraph import CallGraph
from search_technique.Search_technique import Search_technique


class NsgaiiNRE(Search_technique):
    def __init__(self):
        super(NsgaiiNRE, self).__init__()
        self.name = "NsgaiiNRE"

    def select_platform(self, repoName, platform):
        """select to run on local: 1 or on server: 2"""
        if platform == "1":
            'Local'
            jsonFile = "/Users/leichen/Desktop/StaticalAnalysis/" + repoName + ".json"
            repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
            self.outputPath = "/Users/leichen/Desktop/output/"
            callGraph = CallGraph(
                "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName + "/MORCOoutput/csv/callgraph.json")

        elif platform == "2":
            'Server'
            jsonFile = "/home/chenlei/MORCO/extractResult/" + repoName + ".json"
            repoPath = "/home/chenlei/MORCO/data/" + repoName
            self.outputPath = "/home/chenlei/MORCO/output_temp/"
            callGraph = CallGraph("/home/chenlei/MORCO/relationship/" + repoName + "/callgraph.json")

        return jsonFile, repoPath, self.outputPath, callGraph

    def load(self):
        repoName, max_evaluations, platform = self.load_args()
        jsonFile, repoPath, outputPath, callGraph = self.select_platform(repoName, platform)
        jClist = self.load_repository(jsonFile=jsonFile, exclude_test=True, exclude_anonymous=True)

        self.problem = SearchROProblemNRE(jClist, repoPath, callGraph)
        return self

    def search(self):
        self.algorithm = NSGAII(
        problem=self.problem,
        population_size=100,
        offspring_population_size=100,
        mutation=IntegerPolynomialMutation(probability=0.5),
        crossover=IntegerSBXCrossover(probability=1),
        termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.observable.register(observer=WriteFrontToFileObserver(
            output_directory=self.outputPath + self.repoName + "/front/"+self.name+"/"))
        self.algorithm.run()
        return self

if __name__ =="__main__":
    nsgaiiNRE = NsgaiiNRE()
    nsgaiiNRE.load().search().write_result()
