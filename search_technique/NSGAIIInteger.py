import sys

sys.path.append('../')
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import readJson
from jxplatform2.jClass import jClass
from SearchROProblemInteger import SearchROProblemInteger
from jmetal.util.observer import WriteFrontToFileObserver, BasicObserver
from code_ownership.DeveloperGraph import DeveloperGraph
from code_ownership.PullRequestService import PullRequestService


def load_args():
    'Read Jxplatform2 extraction result'
    repoName = sys.argv[1]
    max_evaluations = sys.argv[2]
    platform = sys.argv[3]
    return repoName, max_evaluations, platform


def select_platform(repoName, platform):
    """select to run on local: 1 or on server: 2"""
    if platform == "1":
        'Local'
        max_evaluations = 1000
        repoName = "mbassador"
        jsonFile = "/Users/leichen/Desktop/" + repoName + ".json"
        repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
        outputPath = "/Users/leichen/Desktop/output"
        # load developer relationship
        relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/pullrequest.csv"
        res = PullRequestService().loadPullRequest(relationshipCsvPath)
        developerGraph = DeveloperGraph(res).generate_vertices().build()
        ownershipPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName + "/MORCOoutput/csv/ownership.csv"

    elif platform == "2":
        'Server'
        jsonFile = "/home/chenlei/MORCO/extractResult/" + repoName + ".json"
        repoPath = "/home/chenlei/MORCO/data/" + repoName
        outputPath = "/home/chenlei/MORCO/output_temp/"
        # load developer relationship
        relationshipCsvPath = "/home/chenlei/MORCO/relationship/" + repoName + "/pullrequest.csv"
        res = PullRequestService().loadPullRequest(relationshipCsvPath)
        developerGraph = DeveloperGraph(res).generate_vertices().build()
        ownershipPath = "/home/chenlei/MORCO/relationship/" + repoName + "/ownership.csv"

    return jsonFile, repoPath, outputPath, developerGraph, ownershipPath


def exclude_test_class(exclude: bool, javaClasses):
    """exclude is true, then exclude test_class"""
    res = []
    if exclude:
        for each in javaClasses:
            if not each.testClass:
                res.append(each)
    else:
        for each in javaClasses:
            res.append(each)
    return res


def json_2_jClass(jsonList):
    res = []
    for each in jsonList:
        res.append(jClass(each))
    return res


def load_repository(jsonFile: str, exclude_test: bool):
    # load repository class info
    load = readJson(jsonFile)
    javaClasses = json_2_jClass(load)
    return exclude_test_class(exclude=exclude_test, javaClasses=javaClasses)


repoName, max_evaluations, platform = load_args()
jsonFile, repoPath, outputPath, developerGraph, ownershipPath = select_platform(repoName, platform)
jClist = load_repository(jsonFile=jsonFile, exclude_test=True)

problem = SearchROProblemInteger(jClist, repoPath, developerGraph, ownershipPath)

algorithm = NSGAII(
    problem=problem,
    population_size=300,
    offspring_population_size=300,
    mutation=IntegerPolynomialMutation(probability=0.5),
    crossover=IntegerSBXCrossover(probability=1),
    termination_criterion=StoppingByEvaluations(max_evaluations=int(max_evaluations))
)

algorithm.observable.register(observer=BasicObserver())
algorithm.observable.register(observer=WriteFrontToFileObserver(
    output_directory=outputPath + repoName + "/front"))
algorithm.run()
front = get_non_dominated_solutions(algorithm.get_result())

# save to files
print_function_values_to_file(front, outputPath + repoName + '/FUN.NSGAII.SearchRO')
print_variables_to_file(front, outputPath + repoName + '/VAR.NSGAII.SearchRO')

print('Algorithm (continuous problem): ' + algorithm.get_name())
print('Problem: ' + problem.get_name())
print('Computing time: ' + str(algorithm.total_computing_time))
