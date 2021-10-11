from problem import FindOperations
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import BitFlipMutation,SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import readJson
from Jxplatform2.jClass import jClass
from RefactoringOperation import Solution
from CodeOwnership.Repository import Repository

from Jxplatform2.Jxplatform2 import Jxplatform2

'use Jxplatform2 extract repository'
j = "/Users/leichen/Code/pythonProject/pythonProject/salabResearch/Jxplatform2/JxplatformExtract.jar"
t = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
c = t
jsonPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador/jmbassador.json"
jxplatform2=Jxplatform2(j,t,c,jsonPath)
jxplatform2.extractInfo()

'Read Jxplatform2 extraction result'
#jsonFileRTE = "/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
load = readJson(jsonPath)
jClist = []
for each in load:
    jClist.append(jClass(load=each))


userName="Benjamin Diedrichsen"

'get ownership csv'
path = t
outputPath = t+"/output"

repo = Repository(path)
repo.countAuthorCommit(outputPath=outputPath)
repo.writeCSV(t+"/csv")


'Encoding'
s = Solution()
s.binaryEncodingFixedLength(jClist)
s.setSoltuionLen()
Qmood=0
problem=FindOperations(Qmood,s,jClist,userName,repo)

algorithm = NSGAII(
    problem=problem,
    population_size=1000,
    offspring_population_size=100,
    mutation=BitFlipMutation(probability=1.0 / problem.number_of_variables),
    # mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    # crossover=SBXCrossover(probability=1.0, distribution_index=20),
    crossover=SPXCrossover(probability=1.0),
    termination_criterion=StoppingByEvaluations(max_evaluations=25000)
)

algorithm.run()

front = get_non_dominated_solutions(algorithm.get_result())

# save to files
print_function_values_to_file(front, 'FUN.NSGAII.SubsetSum')
print_variables_to_file(front, 'VAR.NSGAII.SubsetSum')