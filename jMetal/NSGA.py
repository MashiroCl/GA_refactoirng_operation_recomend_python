from problem import FindOperations
from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation,BitFlipMutation,SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from readJson import readJson
from jClass import jClass
from RefactoringOperation import Solution

'Read Jxplatform2 extraction result'
jsonFileRTE = "/Users/leichen/Code/jxplatform2Json/CKJM_EXT.json"
load = readJson(jsonFileRTE)
jClist = []
for each in load:
    jClist.append(jClass(load=each))

'Encoding'
s = Solution()
s.binaryEncoding(jClist)
s.setSoltuionLen()
Qmood=0
problem=FindOperations(Qmood,s,jClist)

algorithm = NSGAII(
    problem=problem,
    population_size=100,
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