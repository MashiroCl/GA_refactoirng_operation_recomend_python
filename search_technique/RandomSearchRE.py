from jmetal.util.observer import BasicObserver, WriteFrontToFileObserver
from jmetal.util.termination_criterion import StoppingByEvaluations

from Search_technique import Search_technique
from SearchROProblemRE import SearchROProbleRE
from jmetal.algorithm.multiobjective import RandomSearch

from call_graph.CallGraph import CallGraph
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService


class RandomSearchRE(Search_technique):
    '''
    Simple random search with review effort
    Simple random search: call create_solution() to randomly create a new solution in each iteration,
                          if the new soulution is a non-dominated one, it will be recorded in FUN.xx
    '''
    def __init__(self):
        super(RandomSearchRE, self).__init__()
        self.name = "RandomSearchRE"

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
        self.algorithm = RandomSearch(
            problem=self.problem,
            termination_criterion=StoppingByEvaluations(max_evaluations=int(self.max_evaluations))
        )
        self.algorithm.observable.register(observer=BasicObserver())
        self.algorithm.observable.register(observer=WriteFrontToFileObserver(
            output_directory=self.outputPath + self.repoName + "/front/"+self.name+"/"))
        self.algorithm.run()
        return self

if __name__ =="__main__":
    randomSearchRE = RandomSearchRE()
    randomSearchRE.load().search().write_result()
