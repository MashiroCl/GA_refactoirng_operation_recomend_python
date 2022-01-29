import sys
sys.path.append('../')
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator.crossover import IntegerSBXCrossover
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import readJson
from Jxplatform2.jClass import jClass
from SearchROProblemInteger import SearchROProblemInteger
from jmetal.lab.visualization import Plot,InteractivePlot
from jmetal.util.observer import WriteFrontToFileObserver,PlotFrontToFileObserver,ProgressBarObserver,BasicObserver
from CodeOwnership.DeveloperGraph import DeveloperGraph
from CodeOwnership.PullRequestService import PullRequestService

'Read Jxplatform2 extraction result'
# jsonFile = "/Users/leichen/Desktop/jedis.json"
# repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jedis"
# repoName = "ganttproject-1.10.2"
repoName = sys.argv[1]
max_evaluations = sys.argv[2]
platform = sys.argv[3]

if platform == "1":
    'Local'
    max_evaluations = 15000
    repoName = "mbassador"
    jsonFile = "/Users/leichen/Desktop/" +repoName +".json"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName
    outputPath = "/Users/leichen/Desktop/output"

elif platform == "2":
    'Server'
    jsonFile = "/home/chenlei/MORCO/extractResult/" + repoName + ".json"
    repoPath = "/home/chenlei/MORCO/data/" + repoName
    outputPath = "/home/chenlei/MORCO/output_all_objectives_positive/"

#load repository class info
load = readJson(jsonFile)
jClist = []
for each in load:
    jClist.append(jClass(load=each))

#load developer relationship
relationshipCsvPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/MORCOoutput/csv/pullrequest.csv"
res = PullRequestService().loadPullRequest(relationshipCsvPath)
developerGraph = DeveloperGraph(res).generate_vertices().build()

problem = SearchROProblemInteger(jClist,repoPath,developerGraph)

# max_evaluations=5000
algorithm = NSGAII(
    problem=problem,
    population_size=150,
    offspring_population_size=140,
    mutation=IntegerPolynomialMutation(probability=0.5),
    crossover=IntegerSBXCrossover(probability=1),
    termination_criterion=StoppingByEvaluations(max_evaluations=int(max_evaluations))
)

algorithm.observable.register(observer=BasicObserver())
algorithm.observable.register(observer=WriteFrontToFileObserver(
    output_directory=outputPath+repoName+"/front2"))
algorithm.run()
front = get_non_dominated_solutions(algorithm.get_result())
# front = problem.front
# for each in algorithm.get_result():
#     front.append(each)
#
# save to files
print_function_values_to_file(front, outputPath+repoName+'/FUN.NSGAII.SearchRO')
print_variables_to_file(front, outputPath+repoName+'/VAR.NSGAII.SearchRO')

print('Algorithm (continuous problem): ' + algorithm.get_name())
print('Problem: ' + problem.get_name())
print('Computing time: ' + str(algorithm.total_computing_time))