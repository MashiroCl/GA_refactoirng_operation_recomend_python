from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import BitFlipMutation,SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from utils import readJson
from Jxplatform2.jClass import jClass
from SearchROProblemBinary import SearchROProblemBinary


'Read Jxplatform2 extraction result'
jsonFile = "/Users/leichen/Desktop/jedis.json"
load = readJson(jsonFile)
jClist = []
for each in load:
    jClist.append(jClass(load=each))

problem=SearchROProblemBinary(jClist)

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