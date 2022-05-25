from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.util.observer import BasicObserver, WriteFrontToFileObserver
from jmetal.util.termination_criterion import StoppingByEvaluations

from Search_technique import Search_technique
from SearchROProblemRE import SearchROProbleRE
from jmetal.algorithm.multiobjective import MOEAD

from call_graph.CallGraph import CallGraph
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService


class MoeadRE(Search_technique):
    '''
    Multi-Objective evolutionary algorithm by decomposition considering review effort
    Setting the penalty parameter in W3D_300.dat
    '''
    def __init__(self):
        super(MoeadRE, self).__init__()
        self.name = "MoeadRE"

    def select_platform(self, repoName, platform):
        """select to run on local: 1 or on server: 2"""
        if platform == "1":
            'Local'
            jsonFile = "/Users/leichen/Desktop/StaticalAnalysis/" + repoName + ".json"
            repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
            self.outputPath = "/Users/leichen/Desktop/output/"
            # load developer relationship
            relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName + "/MORCOoutput/csv/pullrequest.csv"
            res = PullRequestService().loadPullRequest(relationshipCsvPath)
            developerGraph = DeveloperGraph(res).generate_vertices().build()
            ownershipPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName + "/MORCOoutput/csv/ownership.csv"
            callGraph = CallGraph(
                "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName + "/MORCOoutput/csv/callgraph.json")

        elif platform == "2":
            'Server'
            jsonFile = "/home/chenlei/MORCO/extractResult/" + repoName + ".json"
            repoPath = "/home/chenlei/MORCO/data/" + repoName
            self.outputPath = "/home/chenlei/MORCO/output_temp/"
            # load developer relationship
            relationshipCsvPath = "/home/chenlei/MORCO/relationship/" + repoName + "/pullrequest.csv"
            res = PullRequestService().loadPullRequest(relationshipCsvPath)
            developerGraph = DeveloperGraph(res).generate_vertices().build()
            ownershipPath = "/home/chenlei/MORCO/relationship/" + repoName + "/ownership.csv"
            callGraph = CallGraph("/home/chenlei/MORCO/relationship/" + repoName + "/callgraph.json")

        return jsonFile, repoPath, self.outputPath, developerGraph, ownershipPath, callGraph

    def load(self):
        repoName, max_evaluations, platform = self.load_args()
        jsonFile, repoPath, outputPath, developerGraph, ownershipPath, callGraph = self.select_platform(repoName,
                                                                                                        platform)
        jClist = self.load_repository(jsonFile=jsonFile, exclude_test=True, exclude_anonymous=True)

        self.problem = SearchROProbleRE(jClist, repoPath, developerGraph, ownershipPath, callGraph)
        return self

    def search(self):
        self.algorithm = MOEAD(
            problem=self.problem,
            population_size=300,
            mutation=IntegerPolynomialMutation(probability=0.5),
            crossover= IntegerSBXCrossover(probability=1),
            aggregative_function=Tschebycheff(dimension=self.problem.number_of_objectives),
            neighbor_size=20,
            neighbourhood_selection_probability=0.9,
            max_number_of_replaced_solutions=2,
            weight_files_path= ".",
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.observable.register(observer=WriteFrontToFileObserver(
            output_directory=self.outputPath + self.repoName + "/front/"+self.name+"/"))
        self.algorithm.run()
        return self

if __name__ =="__main__":
    moeadRE = MoeadRE()
    moeadRE.load().search().write_result()
